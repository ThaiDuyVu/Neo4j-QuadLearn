// CẢNH BÁO: xóa node demo và mọi quan hệ nối với chúng; không xóa toàn DB.
MATCH (n) WHERE n.demo = true DETACH DELETE n
;
