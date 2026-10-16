USE smart_health_analytics;

CREATE TABLE IF NOT EXISTS users (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  full_name     VARCHAR(100) NOT NULL,
  email         VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS health_records (
  id                 INT AUTO_INCREMENT PRIMARY KEY,
  user_id            INT NOT NULL,
  chronological_age  DOUBLE NOT NULL,
  gender             VARCHAR(10)  NOT NULL,
  weight_kg          DOUBLE NOT NULL,
  height_cm          DOUBLE NOT NULL,
  bmi                DOUBLE NOT NULL,
  waist_cm           DOUBLE NOT NULL,
  pulse              DOUBLE NOT NULL,
  systolic_bp        DOUBLE NOT NULL,
  diastolic_bp       DOUBLE NOT NULL,
  total_cholesterol  DOUBLE NOT NULL,
  hemoglobin         DOUBLE NOT NULL,
  hematocrit         DOUBLE NOT NULL,
  creatinine         DOUBLE NOT NULL,
  uric_acid          DOUBLE NOT NULL,
  smoking_status     VARCHAR(20)  NOT NULL,
  sleep_category     VARCHAR(30)  NOT NULL,
  physical_activity  VARCHAR(30)  NOT NULL,
  biological_age     DOUBLE NOT NULL,
  age_acceleration   DOUBLE NOT NULL,
  risk_points        INT    NOT NULL,
  health_risk        VARCHAR(20) NOT NULL,
  health_score       INT    NOT NULL,
  top_driver         VARCHAR(60),
  created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_records_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_user_date (user_id, created_at)
);
