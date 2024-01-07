from app.database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column



class CompanyInfo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employeename: Mapped[str] = mapped_column(String)
    companyname: Mapped[str] = mapped_column(String)
    industry: Mapped[str] = mapped_column(String)
    companysize: Mapped[int] = mapped_column(Integer)

