-- DROP TABLE measurement ;
-- DROP TABLE measurement_soil_moisture ;
-- DROP TABLE measurement_si1145 ;
-- DROP TABLE measurement_bme680 ;
-- DROP TABLE measurement_scd30 ;
-- DROP TABLE measurement_as7341 ;
-- DROP TABLE measurement_picture ;

CREATE TABLE measurement (
	"owner" varchar(200) NOT NULL,
    create_date timestamptz(6) NOT NULL,
	"label" varchar(200) NULL,
	full_content jsonb NULL,
	CONSTRAINT measurement_pk PRIMARY KEY ("owner", create_date)
);

CREATE TABLE measurement_soil_moisture (
    "owner" varchar(200) NOT NULL,
    create_date timestamptz(6) NOT NULL,
    value_1 numeric(30,12) NULL,
    stdev_1 numeric(30,12) NULL,
    value_2 numeric(30,12) NULL,
    stdev_2 numeric(30,12) NULL,
    value_3 numeric(30,12) NULL,
    stdev_3 numeric(30,12) NULL,
    value_4 numeric(30,12) NULL,
    stdev_4 numeric(30,12) NULL,
    value_5 numeric(30,12) NULL,
    stdev_5 numeric(30,12) NULL,
    value_6 numeric(30,12) NULL,
    stdev_6 numeric(30,12) NULL,
    CONSTRAINT measurement_soil_moisture_pk PRIMARY KEY ("owner", create_date)
);

CREATE TABLE measurement_si1145 (
    "owner" varchar(200) NOT NULL,
    create_date timestamptz(6) NOT NULL,
    sunlight_visible numeric(30,12) NULL,
    stdev_sunlight_visible numeric(30,12) NULL,
    sunlight_uv numeric(30,12) NULL,
    stdev_sunlight_uv numeric(30,12) NULL,
    sunlight_ir numeric(30,12) NULL,
    stdev_sunlight_ir numeric(30,12) NULL,
    CONSTRAINT measurement_si1145_pk PRIMARY KEY ("owner", create_date)
);

CREATE TABLE measurement_bme680 (
    "owner" varchar(200) NOT NULL,
    create_date timestamptz(6) NOT NULL,
    temperature numeric(30,12) NULL,
    stdev_temperature numeric(30,12) NULL,
    pressure numeric(30,12) NULL,
    stdev_pressure numeric(30,12) NULL,
    humidity numeric(30,12) NULL,
    stdev_humidity numeric(30,12) NULL,
    gas_resistance numeric(30,12) NULL,
    stdev_gas_resistance numeric(30,12) NULL,
    CONSTRAINT measurement_bme680_pk PRIMARY KEY ("owner", create_date)
);

CREATE TABLE measurement_scd30 (
    "owner" varchar(200) NOT NULL,
    create_date timestamptz(6) NOT NULL,
    co2_ppm numeric(30,12) NULL,
    stdev_co2_ppm numeric(30,12) NULL,
    temperature numeric(30,12) NULL,
    stdev_temperature numeric(30,12) NULL,
    humidity numeric(30,12) NULL,
    stdev_humidity numeric(30,12) NULL,
    CONSTRAINT measurement_scd30_pk PRIMARY KEY ("owner", create_date)
);

CREATE TABLE measurement_as7341 (
    "owner" varchar(200) NOT NULL,
    create_date timestamptz(6) NOT NULL,
    violet_415nm numeric(30,12) NULL,
    stdev_violet_415nm numeric(30,12) NULL,
    indigo_445nm numeric(30,12) NULL,
    stdev_indigo_445nm numeric(30,12) NULL,
    blue_480nm numeric(30,12) NULL,
    stdev_blue_480nm numeric(30,12) NULL,
    cyan_515nm numeric(30,12) NULL,
    stdev_cyan_515nm numeric(30,12) NULL,
    green_555nm numeric(30,12) NULL,
    stdev_green_555nm numeric(30,12) NULL,
    yellow_590nm numeric(30,12) NULL,
    stdev_yellow_590nm numeric(30,12) NULL,
    orange_630nm numeric(30,12) NULL,
    stdev_orange_630nm numeric(30,12) NULL,
    red_680nm numeric(30,12) NULL,
    stdev_red_680nm numeric(30,12) NULL,
    CONSTRAINT measurement_as7341_pk PRIMARY KEY ("owner", create_date)
);

CREATE TABLE measurement_picture (
    "owner" varchar(200) NOT NULL,
    create_date timestamptz(6) NOT NULL,
    picture_1 bytea NULL,
    CONSTRAINT measurement_picture_pk PRIMARY KEY ("owner", create_date)
);
