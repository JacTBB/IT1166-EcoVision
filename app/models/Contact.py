from app.database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class CompanyInfo(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    employee_name: Mapped[str] = mapped_column(String)
    company_name: Mapped[str] = mapped_column(String)
    company_email: Mapped[str] = mapped_column(String)
    industry: Mapped[str] = mapped_column(String)
    company_size: Mapped[int] = mapped_column(Integer)
