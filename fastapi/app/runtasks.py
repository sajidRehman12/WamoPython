from celery_app import add, send_email
 
# Fire and forget
add.delay(4, 6)
 
# Get result
result = add.delay(10, 20)
print(result.get(timeout=10))  # 30
 
# Call email task
send_email.delay("user@example.com", "Hello", "Welcome!")
 
