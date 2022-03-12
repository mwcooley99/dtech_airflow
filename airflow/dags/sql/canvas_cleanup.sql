-- Must add each canvas table that has "hard deletes"
delete from raw_canvas.terms where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
delete from raw_canvas.outcome_results where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
delete from raw_canvas.courses where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
delete from raw_canvas.enrollments where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
delete from raw_canvas.sections where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
delete from raw_canvas.users where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';

-- Add columns
-- TODO: confirm cutoff date is still in use
alter table raw_canvas.terms 
add column if not exists
cut_off_date timestamp without time zone;

-- Add indices
create index if not exists ix_enrollment_id on raw_canvas.courses (enrollment_term_id)
create index if not exists ix_enrollment_id on raw_canvas.courses (enrollment_term_id)
create index if not exists ix_enrollment_id on raw_canvas.courses (enrollment_term_id)
create index if not exists ix_enrollment_id on raw_canvas.courses (enrollment_term_id)
create index if not exists ix_enrollment_id on raw_canvas.courses (enrollment_term_id)
create index if not exists ix_enrollment_id on raw_canvas.courses (enrollment_term_id)
