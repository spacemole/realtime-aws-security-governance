# run custodian:

	python -m venv custodian
	.\custodian\Scripts\Activate.ps1
	pip install c7n


# run policy:

	$Env:AWS_ACCESS_KEY_ID="INSERT_KEY_HERE"; $Env:AWS_SECRET_ACCESS_KEY="INSERT_KEY_HERE" ; $Env:AWS_DEFAULT_REGION="INSERT_REGION_HERE" ; custodian run --output-dir=. INSERT_FILENAME_HERE.yml


