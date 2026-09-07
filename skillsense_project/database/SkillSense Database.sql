create database skillsense;
use skillsense;
show databases;
create table officials (
    official_id int primary key auto_increment,
    name varchar(100) not null,
    department varchar(100),
    designation varchar(100),
    role varchar(100),
    experience_years int,
    education varchar(150)
);
describe officials;
INSERT INTO officials 
(name, department, designation, role, experience_years, education) 
VALUES
('Arjun Mehta', 'Finance', 'Chief Financial Officer', 'Strategic financial planning and risk management', 15, 'MBA in Finance - IIM Ahmedabad'),
('Priya Sharma', 'Human Resources', 'HR Director', 'Talent acquisition, employee relations, and policy framing', 12, 'Master of Human Resource Management'),
('Dr. Rajesh Kumar', 'Public Health', 'Chief Medical Officer', 'Overseeing healthcare initiatives and clinical compliance', 18, 'MD in Community Medicine'),
('Sneha Kulkarni', 'Information Technology', 'Chief Information Security Officer', 'Managing enterprise cybersecurity and cloud infrastructure', 10, 'B.Tech in Computer Science, CISSP Certified'),
('Vikram Singh', 'Operations', 'Operations Manager', 'Supply chain optimization and logistics oversight', 8, 'B.Tech + MBA in Operations'),
('Ananya Das', 'Legal Affairs', 'Legal Counsel', 'Contract drafting, regulatory compliance, and dispute resolution', 6, 'LL.M. (Master of Laws)'),
('Amit Verma', 'Public Relations', 'Communications Director', 'Media relations, crisis communication, and brand management', 14, 'Master in Mass Communication');
SELECT * FROM officials;
create table departments (
    department_id int primary key auto_increment,
    department_name varchar(100) not null unique,
    description varchar(255)
);
describe departments;
insert into departments (department_name, description)
values
('Finance', 'Financial planning and management'),
('Human Resources', 'Employee management and talent development'),
('Public Health', 'Healthcare and public health administration'),
('Information Technology', 'Technology, systems and cybersecurity'),
('Operations', 'Supply chain and operational management'),
('Legal Affairs', 'Legal compliance and regulatory matters'),
('Public Relations', 'Communication, media and public relations');
select * from departments;
select * from officials;
alter table officials
add column department_id int;
describe officials;
set sql_safe_updates = 0;

update officials
set department_id = 1
where department = 'Finance';

update officials
set department_id = 2
where department = 'Human Resources';

update officials
set department_id = 3
where department = 'Public Health';

update officials
set department_id = 4
where department = 'Information Technology';

update officials
set department_id = 5
where department = 'Operations';

update officials
set department_id = 6
where department = 'Legal Affairs';

update officials
set department_id = 7
where department = 'Public Relations';
select official_id, name, department, department_id
from officials;
create table competencies (
    competency_id int primary key auto_increment,
    competency_name varchar(100) not null,
    description varchar(255),
    level varchar(50)
);
describe competencies;
insert into competencies (competency_name, description, level)
values
('financial analysis', 'understanding financial data and making informed decisions', 'advanced'),
('talent management', 'managing employees, recruitment and development', 'advanced'),
('public health management', 'managing healthcare programs and compliance', 'advanced'),
('cybersecurity', 'protecting systems, data and digital infrastructure', 'advanced'),
('operations management', 'managing supply chains and operational processes', 'intermediate'),
('legal compliance', 'understanding laws, regulations and compliance requirements', 'intermediate'),
('communication management', 'managing media, communication and public relations', 'advanced');
select* from competencies;
create table assessments (
    assessment_id int primary key auto_increment,
    official_id int,
    assessment_name varchar(100),
    assessment_date date,
    score decimal(5,2)
);
describe assessments;
insert into assessments (official_id, assessment_name, assessment_date, score)
values
(1, 'financial skills assessment', '2026-09-01', 82.50),
(2, 'hr skills assessment', '2026-09-01', 76.00),
(3, 'public health assessment', '2026-09-01', 91.00),
(4, 'cybersecurity assessment', '2026-09-02', 68.50),
(5, 'operations assessment', '2026-09-02', 79.00),
(6, 'legal compliance assessment', '2026-09-02', 85.50),
(7, 'communication assessment', '2026-09-02', 73.00);
select* from assessments;
create table questions (
    question_id int primary key auto_increment,
    competency_id int,
    question_text varchar(500),
    correct_answer varchar(255),
    difficulty varchar(50)
);
describe questions;
insert into questions (competency_id, question_text, correct_answer, difficulty)
values
(1, 'what is the main purpose of financial risk management?', 'to identify and reduce financial risks', 'medium'),
(2, 'what is an important part of talent management?', 'employee development', 'medium'),
(3, 'what is the main goal of public health management?', 'protecting and improving population health', 'medium'),
(4, 'what is a strong way to protect an organization from cyber threats?', 'regular security monitoring', 'hard'),
(5, 'what is a key objective of supply chain management?', 'efficient movement of goods and resources', 'medium'),
(6, 'what is the purpose of regulatory compliance?', 'to ensure laws and regulations are followed', 'medium'),
(7, 'what is an important part of public relations?', 'effective communication with the public', 'easy');
select* from questions;
create table responses (
    response_id int primary key auto_increment,
    assessment_id int,
    question_id int,
    answer_given varchar(255),
    is_correct boolean
);
describe responses;
insert into responses (assessment_id, question_id, answer_given, is_correct)
values
(1, 1, 'to identify and reduce financial risks', true),
(2, 2, 'employee development', true),
(3, 3, 'protecting and improving population health', true),
(4, 4, 'strong passwords', false),
(5, 5, 'efficient movement of goods and resources', true),
(6, 6, 'to ensure laws and regulations are followed', true),
(7, 7, 'social media', false);
select* from responses;
create table competency_passport (
    passport_id int primary key auto_increment,
    official_id int,
    competency_id int,
    competency_score decimal(5,2),
    competency_level varchar(50)
);
show tables;
describe competency_passport;
insert into competency_passport (official_id, competency_id, competency_score, competency_level)
values
(1, 1, 82.50, 'advanced'),
(2, 2, 76.00, 'intermediate'),
(3, 3, 91.00, 'advanced'),
(4, 4, 68.50, 'intermediate'),
(5, 5, 79.00, 'intermediate'),
(6, 6, 85.50, 'advanced'),
(7, 7, 73.00, 'intermediate');
select* from competency_passport;

select
    o.name as official_name,
    c.competency_name as competency_name,
    cp.competency_score as competency_score,
    cp.competency_level as competency_level
from competency_passport cp
join officials o on cp.official_id = o.official_id
join competencies c on cp.competency_id = c.competency_id;

select
    o.name as official_name,
    c.competency_name as competency_name,
    cp.competency_score as competency_score,
    cp.competency_level as competency_level
from competency_passport cp
join officials o on cp.official_id = o.official_id
join competencies c on cp.competency_id = c.competency_id
where cp.competency_score < 75;

select
    o.name as official_name,
    c.competency_name as competency_name,
    cp.competency_score as competency_score,
    cp.competency_level as competency_level
from competency_passport cp
join officials o on cp.official_id = o.official_id
join competencies c on cp.competency_id = c.competency_id
where cp.competency_score >= 80;

select
    avg(competency_score) as average_competency_score
from competency_passport;

select
    round(avg(competency_score), 2) as average_competency_score
from competency_passport;
show tables;
describe departments;
describe officials;
describe competencies;
describe assessments;
describe questions;
describe responses;
describe competency_passport;
alter table officials
add constraint fk_official_department
foreign key (department_id)
references departments(department_id);

alter table assessments
add constraint fk_assessment_official
foreign key (official_id)
references officials(official_id);

alter table questions
add constraint fk_question_competency
foreign key (competency_id)
references competencies(competency_id);

alter table responses
add constraint fk_response_assessment
foreign key (assessment_id)
references assessments(assessment_id);

alter table responses
add constraint fk_response_question
foreign key (question_id)
references questions(question_id);

alter table competency_passport
add constraint fk_passport_official
foreign key (official_id)
references officials(official_id);

alter table competency_passport
add constraint fk_passport_competency
foreign key (competency_id)
references competencies(competency_id);

show create table officials;
show create table assessments;
show create table questions;
show create table responses;
show create table competency_passport;

insert into assessments
(official_id, assessment_name, assessment_date, score)
values
(999, 'test assessment', '2026-09-04', 50.00);

insert into questions
(competency_id, question_text, correct_answer, difficulty)
values
(999, 'test question', 'test answer', 'easy');

select
    o.official_id,
    o.name,
    d.department_name
from officials o
join departments d
    on o.department_id = d.department_id;
    
    select official_id, name, department, department_id
from officials;

select department_id, department_name
from departments;

select
    official_id,
    name,
    department,
    department_id
from officials
order by official_id;