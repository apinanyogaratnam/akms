start:
	uvicorn api.main:app --reload

create_db:
	python create_api_keys_db.py
