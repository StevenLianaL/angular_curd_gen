use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use axum::response::Response;
use game::create_app;
use tower::util::ServiceExt;
use http_body_util::BodyExt;
use serde_json::{json, Value};

async fn post_response(method: &str, url: &str, req_body: String) -> Response {
    let app = create_app().await;

    let response = app
        .oneshot(
            Request::builder()
                .method(method)
                .uri(url)
                .header("content-type", "application/json")
                .body(Body::from(req_body))
                .unwrap(),
        )
        .await
        .unwrap();
    response
}

#[tokio::test]
async fn test_login() {
    // 200
    let json = json!(
        {
            "username": "test",
            "password": "123",
        });
    let response = post_response("POST", "/auth/login", json.to_string()).await;
    assert_eq!(response.status(), StatusCode::OK);

    // user not found
    let json = json!(
        {
            "username": "test1",
            "password": "1233",
        }
    );
    let response = post_response("POST", "/auth/login", json.to_string()).await;
    let body = response.into_body().collect().await.unwrap().to_bytes();
    let body: Value = serde_json::from_slice(&body).unwrap();
    assert_eq!(body, json!({ "detail": "User test1 not found" }));


    // password error
    let json = json!(
        {
            "username": "test",
            "password": "1233",
        }
    );
    let response = post_response("POST", "/auth/login", json.to_string()).await;
    let body = response.into_body().collect().await.unwrap().to_bytes();
    let body: Value = serde_json::from_slice(&body).unwrap();
    assert_eq!(body, json!({ "detail": "密码错误" }));
}
