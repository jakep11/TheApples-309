Drop database cpe_309;
Create database cpe_309;
Use cpe_309;
-- Description: Stores information and role type for each user of the system
CREATE TABLE Users (
	id INT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(32),
	last_name VARCHAR(32),
	username VARCHAR(32),
	password_hash VARCHAR(64),
	role VARCHAR(12),
	PRIMARY KEY(id)
);

-- Description: Stores all faculty available to work 
CREATE TABLE Faculty (
	id INT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(32),
	last_name VARCHAR(32),
	allowed_work_units INT,
	PRIMARY KEY(id)
);

-- Description: Stores all courses taught by the University
CREATE TABLE Courses (
	id INT NOT NULL AUTO_INCREMENT,
	number INT,
	major VARCHAR(12), -- e.g. CPE
	lecture_workload_units INT,
	lecture_hours INT,
	lab_workload_units INT,
	lab_hours INT,
	PRIMARY KEY(id)
);

-- Description: Stores the terms taught by the University
CREATE TABLE Terms (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(15), -- "Spring 2017"
	PRIMARY KEY(id)
); 

-- Description: Stores all rooms with type and capacity
CREATE TABLE Rooms (
	id INT NOT NULL AUTO_INCREMENT,
	type VARCHAR(32),
	capacity INT,
	PRIMARY KEY(id)
);

-- Description: Stores all sections that have occurred and are planned on the schedule
CREATE TABLE Sections (
	id INT NOT NULL AUTO_INCREMENT,
	course INT,
	term INT,
	number INT,
	section_type VARCHAR(7), -- lecture or lab
	faculty INT,
	room INT,
	time_start TIME,
	time_end TIME, 
	days VARCHAR(3), -- ‘MWF’ or ‘TR’
	PRIMARY KEY(id),
	FOREIGN KEY(course) REFERENCES Courses(id),
	FOREIGN KEY(term) REFERENCES Terms(id),
	FOREIGN KEY(faculty) REFERENCES Faculty(id),
	FOREIGN KEY(room) REFERENCES Rooms(id)
);

-- Description: Stores all equipment types that will be used in various rooms
CREATE TABLE Equipment (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(32),
	PRIMARY KEY(id)
);

-- Description: Stores what equipment is required in each room type
CREATE TABLE RoomEquipment (
	room_type INT,
	equipment INT,
	FOREIGN KEY(equipment) REFERENCES Equipment(id)
);

-- Description: Stores the course and section enrollment/waitlist information for what was actually offered by the University in previous quarters
CREATE TABLE ScheduleFinal ( -- number of sections and capacity from previous terms
	term INT,
	course INT,
	number_sections INT,
	total_enrollment INT,
	total_waitlist INT,
	PRIMARY KEY(term, course),
	FOREIGN KEY(term) REFERENCES Terms(id)
);

-- Description: Stores all of the sections that are planned in a specific term
CREATE TABLE ScheduleInitial (
	term INT,
	section INT
);

-- Description: Stores which tentative schedules have been ‘published’
CREATE TABLE PublishedSchedule (
	term INT
);

-- Description: Stores faculty preferences for what days and times they would like to teach in a specific term 
CREATE TABLE FacultyPreferences (
	faculty INT,
	term INT,
	day CHARACTER(1), -- ‘M’ or ‘T’ etc.
	time_start TIME,
	time_end TIME,
	preference VARCHAR(15),
	FOREIGN KEY(faculty) REFERENCES Faculty(id)
);

-- Description: Stores what classes a faculty is allowed to teach
CREATE TABLE FacultyConstraint (
	faculty INT,
	term INT,
	course INT,
	constraint VARCHAR(32), -- ’Not allowed’ or ‘Not desirable’ or ‘Allowed’
	FOREIGN KEY(faculty) REFERENCES Faculty(id),
	FOREIGN KEY(course) REFERENCES Courses(id),
	FOREIGN KEY(term) REFERENCES Terms(id)
);

CREATE TABLE Comments (
	username VARCHAR(32),
	comment BLOB,
	term INT,
	time TIME,
	FOREIGN KEY(term) REFERENCES Terms(id)
);

CREATE TABLE Notifications (
	id INT NOT NULL AUTO_INCREMENT,
	from_faculty INT, -- Faculty
	message TEXT,
	unread TINYINT(1),
	time TIME,
	PRIMARY KEY(id),
	FOREIGN KEY(from_faculty) REFERENCES Faculty(id)
);

