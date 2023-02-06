docker_run:
	docker run -p 8501:8501 tiniworld/test
docker_build:
	docker build -t tiniworld/test .
run:
	streamlit run webapp/0_🏠_Home.py
