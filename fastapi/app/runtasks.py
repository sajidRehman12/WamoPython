from celery_app import add, send_email
 
add.delay(4, 6)
 
result = add.delay(10, 20)
print(result.get(timeout=10))  # 30
 
send_email.delay("user@example.com", "Hello", "Welcome!")
 
