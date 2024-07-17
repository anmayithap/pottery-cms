.PHONY: merge-dotenv

merge-dotenv:
	python manage.py merge_dotenv

collect-static: merge-dotenv
	python manage.py collectstatic --no-input
