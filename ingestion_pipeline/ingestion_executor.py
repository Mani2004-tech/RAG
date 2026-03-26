from langsmith import traceable


@traceable(name="ingestion_pipeline_execution", run_type="chain")
def execute_ingestion(pipeline, data):
    return pipeline.run(data)