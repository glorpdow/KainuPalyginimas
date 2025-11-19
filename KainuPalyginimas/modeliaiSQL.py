from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# This creates the Base class that we use to define tables.
Base = declarative_base()


class Product(Base):
    """
    Saves the product the user searched for.
    Example: "Milk", "Coca Cola", "Eggs"
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship so we can do product.results to get all scraped results
    results = relationship("PriceResult", back_populates="product")



class PriceResult(Base):
    """
    Saves each scraped result:
    - Product ID
    - Store name ("Rimi", "Maxima", "Iki")
    - Price found on that store's website
    - URL of the product (optional)
    """
    __tablename__ = "price_results"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    store_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    url = Column(String, nullable=True)

    # Allows us to access the product from a result (result.product)
    product = relationship("Product", back_populates="results")
