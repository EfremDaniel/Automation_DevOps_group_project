with src_job_description as (select * from {{ ref('src_job_description') }})

select
    id as job_description_id,
    max (headline) as headline,
    max (description_text) as description_text,
    max (description_html) as description_html
from src_job_description
group by id