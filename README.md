This guide here assumes that you are using are familiar with using the command line, and 

# Creating a new GCP account
 
Steps in this section can be skipped if you already have an existing GCP account
 
## Creating a new trial GCP account

Go to console.cloud.google.com to create your a trial GCP account. If you previously used a trial account, and the trial is over, you can create a new Gmail account.

## Creating a new project on GCP

After logging into the GCP console, create a new project by clicking on the **Select a project** dropdown on the navbar, followed by clicking on **New Project**

While creating a new project, take note of the Project ID. You will need it later.

## Enabling BigQuery and BigQuery Data Transfer API

Search for BigQuery on the navbar, and select the BigQuery (Data warehouse/analytics) feature. You should see an option to select the project you just created.

Repeat the step for the BigQuery Data Transfer API.

# Preparing input table

## Accessing the dataset and table

Go to https://console.cloud.google.com/bigquery?project={PROJECT_ID}&p=bigquery-public-data&d=geo_international_ports&t=world_port_index&page=table, replace {PROJECT_ID} with the Project ID you saved in Create a new Project on GCP step, or use an existing project you already own.

## Create a dataset

Create a new dataset by clicking on the three dots (more options) button on the project in the Explorer. Once done, provide a Dataset ID. You may use `geo_international_ports` just for consistency. Do remember the name set for Dataset ID.

## Copying the table to your project's dataset

Click on copy, select the correct project, and fill in the Dataset and Table fields. Do save both Dataset and Table, as you will need them later.

Click on the copy button at the end to complete this transaction.

## Verify copying job

Once you are notified that the table has been copied, expand the projects on the Explorer. There should be a new table called `world_ports_index`


# Setting up gcloud credentials to execute scripts
Note: I've been using Linux to prepare this assignment, and the commands used below may not work for you if you are on a different OS.

## Downloading, installing and initializing the gcloud CLI

Follow the steps [here](https://cloud.google.com/sdk/docs/install-sdk) to download, install and initialize gcloud CLI.

While initializing the gcloud CLI, you will be prompted to log in and select a project. Select the project that was created earlier.

## Creating a service account

Export your project ID by executing the following

```bash
export PROJECT_ID=$(gcloud config get-value core/project)
```

Create a service account by executing the following. This will create a service account named `bigquery-assignment`. If you choose a different name, do take note and make the necessary changes in the following commands

```bash
gcloud iam service-accounts create bigquery-assignment --display-name "bigquery-assignment"

```

Add the role of bigquery data editor to the service account.

```bash
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member "serviceAccount:bigquery-assignment@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role "roles/bigquery.user" 
  
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member "serviceAccount:bigquery-assignment@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role "roles/bigquery.dataEditor"
```

## Creating service account json file

List the keys associated with the service account and copy the KEY_ID

```bash
gcloud iam service-accounts keys list --iam-account=bigquery-assignment@${PROJECT_ID}.iam.gserviceaccount.com
```

Create a service accounts credentials json file by executing the following, replaceing the KEY_ID by what was copied from the previous step. The `key.json` file will be created in the directory you are currently in. Take note of where this file is stored, as you will need it to run the scripts in this assignment submission.

```bash
gcloud iam service-accounts keys create "./key.json" \
    --iam-account bigquery-assignment@${PROJECT_ID}.iam.gserviceaccount.com
```

# Executing the scripts

The following guide assumes that you have pyenv and pyenv-virtualenv installed, and you have installed Python v3.10.15 using pyenv.
You can visit the [pyenv GitHub page](https://github.com/pyenv/pyenv#installation) for installation instructions, and the [pyenv-virutalenv](https://github.com/pyenv/pyenv#installation) GitHub page on how to install the plugin.

## Setting up the virtual environment

Execute the following to create a virtual environment
```bash
pyenv virtualenv 3.10.15 fp
```

Activate the virtual environment
```bash
pyenv activate fp
```

Update pip and install dependencies
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

## Running the scripts

The Python scripts prefixed by numbers refer to the assignment questions.
Running these scripts without any arguments will throw an error, and provide a brief explanation on the required parameters.
Generally, you will need the `service_account_key_path`, the `PROJECT_ID`, the `dataset` which the script should work with, the name of the `input_table`, and the name of the `output_table`.

If you followed the instructions above, you should be able to execute the following scripts as is.


#### Question 1
What are the 5 nearest ports to the JURONG ISLAND port?
```bash
python3 1_nearest_ports.py \
    --service_account_key_path="./key.json" \
    --project_id=$PROJECT_ID \
    --dataset=geo_international_ports \
    --input_table=world_port_index  \
    --output_table=nearest_ports
```

#### Question 2
What is the country with the largest number of ports with cargo wharves?
```bash
python3 2_largest_number_of_ports \
    --service_account_key_path="./key.json" \
    --project_id=$PROJECT_ID \
    --dataset=geo_international_ports \
    --input_table=world_port_index  \
    --output_table=country_with_most_ports_with_cargo_whaves
```

#### Question 3
What is the nearest port to the coordinates (32.610982, -38.706256), and has access to provisions, water, fuel_oil, and diesel?

```bash
python3 2_largest_number_of_ports \
    --service_account_key_path="./key.json" \
    --project_id=$PROJECT_ID \
    --dataset=geo_international_ports \
    --input_table=world_port_index  \
    --output_table=country_with_most_ports_with_cargo_whaves
```
