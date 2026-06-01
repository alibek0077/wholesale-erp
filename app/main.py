from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Product, Customer, WarehouseItem
from app.database import engine
from app.database import Base
import app.models


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-123"
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": None
        }
    )


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()

    db.close()

    if user:

        request.session["user"] = user.username

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": "Invalid username or password"
        }
    )


@app.get("/dashboard")
async def dashboard(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    total_products = db.query(Product).count()
    total_customers = db.query(Customer).count()
    total_warehouse = db.query(WarehouseItem).count()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_products": total_products,
            "total_customers": total_customers,
            "total_warehouse": total_warehouse
        }
    )


@app.get("/health")
async def health():
    return {"status": "ok"}



@app.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/", status_code=303)

@app.get("/products")
async def products(request: Request):

    db = SessionLocal()

    try:
        products = db.query(Product).all()

        return templates.TemplateResponse(
            request=request,
            name="products.html",
            context={
                "products": products
            }
        )

    finally:
        db.close()

@app.post("/products/add")
async def add_product(
    request: Request,
    name: str = Form(...),
    category: str = Form(...),
    quantity: int = Form(...)
):

    db = SessionLocal()

    product = Product(
        name=name,
        category=category,
        quantity=quantity
    )

    db.add(product)

    db.commit()

    db.close()

    return RedirectResponse(
        "/products",
        status_code=303
    )


@app.get("/products/delete/{product_id}")
async def delete_product(
    product_id: int,
    request: Request
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product:
        db.delete(product)
        db.commit()

    db.close()

    return RedirectResponse(
        "/products",
        status_code=303
    )


@app.post("/products/update/{product_id}")
async def update_product(
    product_id: int,
    request: Request,
    name: str = Form(...),
    category: str = Form(...),
    quantity: int = Form(...)
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product:

        product.name = name
        product.category = category
        product.quantity = quantity

        db.commit()

    db.close()

    return RedirectResponse(
        "/products",
        status_code=303
    )


@app.get("/products/edit/{product_id}")
async def edit_product_page(
    product_id: int,
    request: Request
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    db.close()

    return templates.TemplateResponse(
        "edit_product.html",
        {
            "request": request,
            "product": product
        }
    )


@app.get("/customers")
async def customers_page(request: Request):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    customers = db.query(Customer).all()

    db.close()

    return templates.TemplateResponse(
    request=request,
    name="customers.html",
    context={
        "customers": customers
    }
)


@app.post("/customers/add")
async def add_customer(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...)
):

    db = SessionLocal()

    customer = Customer(
        name=name,
        phone=phone,
        email=email
    )

    db.add(customer)

    db.commit()

    db.close()

    return RedirectResponse(
        "/customers",
        status_code=303
    )


@app.get("/customers/delete/{customer_id}")
async def delete_customer(
    customer_id: int,
    request: Request
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer:
        db.delete(customer)
        db.commit()

    db.close()

    return RedirectResponse(
        "/customers",
        status_code=303
    )


@app.get("/customers/edit/{customer_id}")
async def edit_customer_page(
    customer_id: int,
    request: Request
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    db.close()

    return templates.TemplateResponse(
        "edit_customer.html",
        {
            "request": request,
            "customer": customer
        }
    )


@app.post("/customers/update/{customer_id}")
async def update_customer(
    customer_id: int,
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...)
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer:

        customer.name = name
        customer.phone = phone
        customer.email = email

        db.commit()

    db.close()

    return RedirectResponse(
        "/customers",
        status_code=303
    )


@app.get("/warehouse")
def warehouse_page(request: Request):

    db = SessionLocal()

    warehouse_items = db.query(WarehouseItem).all()

    db.close()

    return templates.TemplateResponse(
    request=request,
    name="warehouse.html",
    context={
        "warehouse_items": warehouse_items
    }
)


@app.post("/warehouse/add")
async def add_warehouse_item(
    request: Request,
    product: str = Form(...),
    location: str = Form(...),
    stock: int = Form(...)
):

    db = SessionLocal()

    item = WarehouseItem(
        product=product,
        location=location,
        stock=stock
    )

    db.add(item)

    db.commit()

    db.close()

    return RedirectResponse(
        "/warehouse",
        status_code=303
    )


@app.get("/warehouse/delete/{item_id}")
async def delete_warehouse_item(
    item_id: int,
    request: Request
):

    if "user" not in request.session:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    item = db.query(WarehouseItem).filter(
        WarehouseItem.id == item_id
    ).first()

    if item:
        db.delete(item)
        db.commit()

    db.close()

    return RedirectResponse(
        "/warehouse",
        status_code=303
    )
