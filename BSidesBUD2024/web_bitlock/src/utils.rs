use base64::{prelude::*, DecodeError};
use regex::Regex;

pub fn decrypt(ciphertext: &str, key: &str) -> Result<String, DecodeError> {
    let ciphertext = BASE64_STANDARD.decode(ciphertext)?;
    let mut plaintext = String::new();

    // simple repeated xor
    for (i, ch) in ciphertext.iter().enumerate() {
        let key_char = key.chars().nth(i % key.len()).unwrap() as u8;
        let decrypted_char = (*ch ^ key_char) as char;

        plaintext.push(decrypted_char);
    }

    Ok(plaintext)
}

// Gotta remove some dangerous things.
pub fn remove_sql_keywords(data: &str) -> String {
    let pattern = Regex::new("(?i)(UNION|SELECT|AND|UPDATE)").unwrap();

    return pattern.replace_all(data, "").into_owned();
}
