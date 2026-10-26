import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

# 1. Load key safely using relative pathing
load_dotenv(dotenv_path=".env")
STRIPE_API_KEY = os.getenv("STRIPE_TEST_KEY")

app = FastAPI(title="Stripe Customer Creation UI")


# 2. Render HTML Form Page
@app.get("/", response_class=HTMLResponse)
def show_form():
  return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Create Stripe Customer</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f4f6f9; margin: 0; }
            .card { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 320px; }
            h2 { margin-top: 0; color: #333; }
            label { display: block; margin-top: 15px; font-weight: bold; color: #555; }
            input { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; background-color: #635bff; color: white; border: none; padding: 12px; margin-top: 20px; font-size: 16px; border-radius: 5px; cursor: pointer; font-weight: bold; }
            button:hover { background-color: #4b45c6; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Add Customer</h2>
            <form action="/create-customer" method="POST">
                <label>Full Name:</label>
                <input type="text" name="name" placeholder="e.g. Tarun Verma" required />
                
                <label>Email Address:</label>
                <input type="email" name="email" placeholder="e.g. tarun@example.com" required />
                
                <button type="submit">Submit to Stripe</button>
            </form>
        </div>
    </body>
    </html>
    """


# 3. Handle Form Submission & Execute POST to Stripe
@app.post("/create-customer", response_class=HTMLResponse)
def handle_create_customer(name: str = Form(...), email: str = Form(...)):
  url = "https://api.stripe.com/v1/customers"
  headers = {
      "Authorization": f"Bearer {STRIPE_API_KEY}",
      "Content-Type": "application/x-www-form-urlencoded",
  }

  payload = {
      "name": name,
      "email": email,
      "description": "Created via simple FastAPI Web UI",
  }

  response = httpx.post(url, headers=headers, data=payload)

  if response.status_code == 200:
    data = response.json()
    return f"""
        <html>
            <body style="font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f4f6f9;">
                <div style="background: white; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h2 style="color: #2e7d32;">✅ Customer Created Successfully!</h2>
                    <p><strong>Stripe ID:</strong> {data.get("id")}</p>
                    <p><strong>Name:</strong> {data.get("name")}</p>
                    <p><strong>Email:</strong> {data.get("email")}</p>
                    <br/>
                    <a href="/" style="color: #635bff; font-weight: bold; text-decoration: none;">← Add Another Customer</a>
                </div>
            </body>
        </html>
        """
  else:
    return f"""
        <html>
            <body style="font-family: Arial; padding: 50px;">
                <h2 style="color: #d32f2f;">❌ Error Creating Customer</h2>
                <p><strong>HTTP Status:</strong> {response.status_code}</p>
                <pre>{response.text}</pre>
                <a href="/">Try Again</a>
            </body>
        </html>
        """


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("create_customer_ui:app", host="127.0.0.1", port=8000, reload=True)