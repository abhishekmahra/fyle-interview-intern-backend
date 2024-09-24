-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grading_counts AS (
    SELECT 
        teacher_id, 
        COUNT(id) AS graded_count
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
max_grading_teacher AS (
    SELECT 
        teacher_id
    FROM teacher_grading_counts
    ORDER BY graded_count DESC
    LIMIT 1
)
SELECT COUNT(id) AS grade_a_count
FROM assignments
WHERE teacher_id = (SELECT teacher_id FROM max_grading_teacher)
AND grade = 'A'
AND state = 'GRADED';

