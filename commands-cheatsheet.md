# run custodian:

	python -m venv custodian
	.\custodian\Scripts\Activate.ps1
	pip install c7n


# run policy:

	$Env:AWS_ACCESS_KEY_ID="AKIATEMC6PMV4E2WT5NG"; $Env:AWS_SECRET_ACCESS_KEY="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" ; $Env:AWS_DEFAULT_REGION="ap-southeast-2" ; custodian run --output-dir=. sg8.yml

	$Env:AWS_ACCESS_KEY_ID="INSERT_KEY_HERE"; $Env:AWS_SECRET_ACCESS_KEY="INSERT_KEY_HERE" ; $Env:AWS_DEFAULT_REGION="INSERT_REGION_HERE" ; custodian run --output-dir=. INSERT_FILENAME_HERE.yml
