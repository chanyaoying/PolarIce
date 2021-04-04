-- SELECT * FROM ROOM;

-- DROP TABLE ROOMS;

CREATE TABLE ROOM (
    roomid int,
    profid int
)

CREATE TABLE QUESTION (
    questionid int, 
    question VARCHAR, 
    choices VARCHAR, 
    roomid INT
)

SELECT * FROM QUESTION

-- SELECT * FROM ROOM