package databaseservice

import (
	"fmt"
	"os"
	"sync"

	"github.com/leesper/couchdb-golang"
	"github.com/sirupsen/logrus"
)

var instance IService
var once sync.Once

func GetInstance() IService {
	once.Do(func() {
		instance = NewService()
	})
	return instance
}

type DatabaseService struct {
	couchdbClient *couchdb.Server
}

func NewService() IService {
	couchDBUser := os.Getenv("COUCHDB_USER")
	couchDBPassword := os.Getenv("COUCHDB_PASSWORD")
	client, err := couchdb.NewServer(fmt.Sprintf("http://%s:%s@couchdb:5984", couchDBUser, couchDBPassword))
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Fatal("Could not connect to CouchDB")
	}
	return &DatabaseService{
		couchdbClient: client,
	}
}

type IService interface {
	GetDB(dbName string) (*couchdb.Database, error)
}

func (s *DatabaseService) GetDB(dbName string) (*couchdb.Database, error) {
	db, err := s.couchdbClient.Get(dbName)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err":     err,
			"db name": dbName,
		}).Error("Could not get db")
		return nil, err
	}
	return db, nil
}
