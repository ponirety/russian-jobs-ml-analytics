from fastapi import FastAPI
from  pydantic import BaseModel
import pydantic as pyd
from src.predictor import predict_salary, names

app = FastAPI()

class VacancyInput(BaseModel):
    experience: int
    name_length: int
    is_senior: int = 0
    is_junior: int = 0
    employment_full: int = pyd.Field(alias="employment_form_Полная занятость", default=0)
    employment_not_full: int = pyd.Field(alias="employment_form_Частичная занятость", default=0)
    accept_labor_contract: int
    area_moscow: int = pyd.Field(alias="area_name_Москва", default=0)
    category_high_midle_manegment: int = pyd.Field(alias="category_Высший и средний менеджмент", default=0)
    is_field_work: int
    accept_temporary: int
    is_on_site: int
    class Config:
        populate_by_name = True

@app.post("/predict")
def predict(data: VacancyInput):
    data_dict = data.model_dump(by_alias=True)
    for name in names:
        if name not in data_dict:
            data_dict[name] = 0

    result = predict_salary(data_dict)

    return {"predicted_salary": int(round(result))}
    
