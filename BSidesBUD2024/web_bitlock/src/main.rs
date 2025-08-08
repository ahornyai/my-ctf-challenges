use actix_files as fs;
use actix_session::{storage::CookieSessionStore, Session, SessionMiddleware};
use actix_web::{cookie::Key, web, App, Error, HttpResponse, HttpServer};
use askama_actix::Template;
use rusqlite::{Connection, Result};
use serde_json::{self, Value};
use std::env;

mod utils;

// Templates
#[derive(Template)]
#[template(path = "dashboard.html")]
pub struct DashboardTemplate {
    pub flag: String,
}

#[derive(Template)]
#[template(path = "login.html")]
pub struct LoginTemplate;

// Endpoints
pub async fn dashboard(session: Session) -> Result<HttpResponse, Error> {
    let logged_in = session.get::<bool>("logged_in")?.unwrap_or(false);

    if !logged_in {
        return Ok(HttpResponse::Found()
            .append_header(("Location", "/login"))
            .finish());
    }

    let flag = env::var("FLAG").unwrap_or("BSIDES{fake_flag}".to_string());
    let template = DashboardTemplate { flag };

    Ok(HttpResponse::Ok().body(template.render().unwrap()))
}

pub async fn handle_login(
    req_body: String,
    session: Session,
    db: web::Data<Connection>,
) -> HttpResponse {
    // Military grade encryption to stop script kiddies
    let mut body = match utils::decrypt(&req_body, "Porcica1") {
        Ok(decoded) => decoded,
        Err(e) => return HttpResponse::BadRequest().body(e.to_string()),
    };

    // Sanitize the input using poor man's WAF
    body = utils::remove_sql_keywords(body.as_str());

    let object: Value = match serde_json::from_str(&body) {
        Ok(value) => value,
        Err(e) => return HttpResponse::BadRequest().body(e.to_string()),
    };

    let username = object["username"].as_str().unwrap_or("");
    let password = object["password"].as_str().unwrap_or("");

    // Why should I use prepared statements? I can just use format string lol. plaintext password storage ftw
    let mut stmt = match db.prepare(
        format!("SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
            .as_str(),
    ) {
        Ok(stmt) => stmt,
        Err(e) => return HttpResponse::InternalServerError().body(e.to_string()),
    };
    let mut users = stmt.query(()).unwrap();

    // Check if the results are empty
    if users.next().unwrap().is_none() {
        return HttpResponse::Unauthorized().body("Wrong username or password.");
    }

    if let Some(e) = session.insert("logged_in", true).err() {
        return HttpResponse::InternalServerError().body(e.to_string());
    }

    HttpResponse::Ok().body("Nice job")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let signing_key = Key::generate();

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(Connection::open("users.db").unwrap()))
            .wrap(
                SessionMiddleware::builder(CookieSessionStore::default(), signing_key.clone()).build(),
            )
            .service(fs::Files::new("/static", "static"))
            .route("/", web::get().to(dashboard))
            .route("/login", web::post().to(handle_login))
            .route("/login", web::get().to(|| async { LoginTemplate }))
    })
    .bind(("0.0.0.0", 5858))?
    .run()
    .await
}
