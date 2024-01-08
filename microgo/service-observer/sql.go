package main

import (
	// "database/sql"
)

// func assert(condition bool, message string) error {
// 	if !condition {
// 		msg := fmt.Sprintf("Assertion failed: %s", message)
// 		return errors.New(msg)
// 	}
// 	return nil
// }


// func pingMariaDB() error {
// 	accessUser := os.Getenv("ACCESS_USR")
// 	accessPwd := os.Getenv("ACCESS_PWD")
// 	mariaHost := os.Getenv("MARIADB_HOST")
// 	mariaPort := os.Getenv("MARIADB_PORT")
// 	authDb := os.Getenv("AUTHDB")

// 	uri := fmt.Sprintf("%s:%s@tcp(%s:%v)/%s", accessUser, accessPwd, mariaHost, mariaPort, authDb)

// 	fmt.Println(uri)

// 	db, err := sql.Open("mysql", uri)
// 	if err != nil {
// 		return err
// 	}

// 	defer db.Close()

// 	err = db.Ping()
// 	if err != nil {
// 		return err
// 	}

// 	query := "SELECT COUNT(*) FROM users"

// 	var count int
// 	err = db.QueryRow(query).Scan(&count)
// 	if err != nil {
// 		log.Fatal(err)
// 	}

// 	err = assert(count == 2, "value should be 2")
// 	if err != nil {
// 		log.Printf("%s", err)
// 		return err
// 	}
// 	fmt.Println("MySQL is working properly.")
// 	return nil
// }
