import os
import threading
from logging import getLogger
from typing import List

import psycopg2

from app.core.singleton_pattern import singleton

log = getLogger(__file__)


class psycopg2_hdlr:
    def __init__(self, host, userName, password, dbName, port, identifier):
        self.host = host
        self.user = userName
        self.passwd = password
        self.db = dbName
        self.port = port
        self.isFree = True
        self.id = identifier
        self.err = ""
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database=self.db,
                user=self.user,
                password=self.passwd,
                host=self.host,
                port=self.port,
                cursor_factory=psycopg2.extras.DictCursor,
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except psycopg2.OperationalError as err:
            log.critical(
                "-- <<DB-POOL>> Database Error during connection setup => %s --",
                str(err),
                exc_info=1,
            )
            self.err = err

    def execute(self, qstr, command, *args):
        try:
            print(qstr)
            log.debug(
                "<<<< Executing Query -- %s with dbhndl id=%s", qstr, str(self.id)
            )
            log.debug("Query args:%s", args)
            # if qstr.endswith(";"):
            #     qstr = qstr[:-1]
            self.cursor.execute(qstr, args)
            log.debug(">>>> Executed Query -- %s with dbhndl id=%s", qstr, str(self.id))

        except psycopg2.ProgrammingError as e:
            print(e)
            log.error("--------------------------------")
            log.error(
                "-- Wrong Sql Statement [Exception %s] for dbhndl id=%s--",
                str(e),
                str(self.id),
                exc_info=1,
            )
            log.error("Query:%s", qstr)
            log.error("Query args:%s", args)
            log.error("--------------------------------")
            return "False", e
        except psycopg2.OperationalError as e:
            # "If connection fails then "
            print(e)

            log.critical(
                "-- Database Operational Error - [%s]--for dbhndl id=%s",
                str(e),
                str(self.id),
                exc_info=1,
            )
            if (
                (str(e).lower().find("2003", 1, 8) != -1)
                or (str(e).lower().find("2013", 1, 8) != -1)
                or (str(e).lower().find("2006", 1, 8) != -1)
            ):
                try:
                    log.warn(
                        "** Trying Once Again To Connect The Database for dbhndl id=%s**",
                        str(self.id),
                    )
                    self.connect()
                except Exception as e:
                    return "False", e
                else:
                    log.info(
                        "- - -Connection Restored for dbhndl id=%s- - -", str(self.id)
                    )
                    return self.execute(qstr, command, *args)
            else:
                log.critical(
                    "-- Other Then Connection Lost for dbhndl id=%s- --", str(self.id)
                )
                return "False", e
        except psycopg2.InternalError as e:
            print(e)

            # "The cursor is out of Sync"
            log.error("--------------------------------")
            log.error(
                "-- Exception [%s]--for dbhndl id=%s", str(e), str(self.id), exc_info=1
            )
            log.error("Query:%s", qstr)
            log.error("Query args:%s", args)
            log.error("--------------------------------")
            return "False", e
        except psycopg2.IntegrityError as e:
            print(e)

            log.error("--------------------------------")
            # "a foreign key check fails, duplicate key, etc."
            log.error(
                "-- Exception [%s]--for dbhndl id=%s", str(e), str(self.id), exc_info=1
            )
            log.error("Query:%s", qstr)
            log.error("Query args:%s", args)
            log.error("--------------------------------")
            return "False", e
        except psycopg2.Error as e:
            print(e)

            log.critical(
                "-- Exception [%s]--for dbhndl id=%s", str(e), str(self.id), exc_info=1
            )
            try:
                log.info(
                    "** Trying Once Again To Connect The Database for dbhndl id=%s**",
                    str(self.id),
                )
                self.connect()
            except Exception as e:
                return "False", e
            else:
                log.info("- - -Connection Restored for dbhndl id=%s- - -", str(self.id))
                self.execute(qstr, command, *args)
        except Exception as e:
            log.critical(
                "-- Exception [%s]--for dbhndl id=%s", str(e), str(self.id), exc_info=1
            )
            # self.execute(self, qstr,command, *args)
            return "False", e

        # Query successful
        if command == "SELECT":
            data = self.cursor.fetchall()
            return "True", data
        if command == "SELECT_ONE":
            data = self.cursor.fetchone()
            return "True", data
        elif command == "UPDATE":
            #  Unlock Tables Explicitly
            rowcount = self.cursor.rowcount
            # log.debug("Calling commit() after UPDATE from DB-POOL.py on every successful update")
            # stat,row = self.commit()
            return "True", rowcount
        elif command == "DELETE":
            #  Unlock Tables Explicitly
            rowcount = self.cursor.rowcount
            # stat = self.unlockTables()
            return "True", rowcount
        elif command == "INSERT":
            return "True", "Inserted", self.cursor.fetchone()[0]
        elif command == "EXECUTE":
            return "True", "Executed"
        elif command == "START TRANS":
            return "True", "Started"
        # elif command=='ROLLBACK':
        #    return 'True','Rollback'
        elif command == "COMMIT":
            return "True", "Commit"
        # elif command=='savepoint':
        #    return 'True','savepoint'
        # elif command=='COMMIT TRANS':
        #    return 'True','Transaction Commit'
        # elif command=='ROLLTRANS':
        #    return 'True','Transaction Rolled'
        else:
            log.critical("Unsupported SQL command = %s", command)


@singleton
class dbHdlr:
    def __init__(self):
        self.dbHndlrList: List[psycopg2_hdlr] = []
        self.lock = threading.Lock()
        for i in range(1, int(os.getenv("DATABASE_POOL_SIZE")) + 1):
            dbHndlr_obj = psycopg2_hdlr(
                os.getenv("DATABASE_HOST"),
                os.getenv("DATABASE_USER"),
                os.getenv("DATABASE_PASSWORD"),
                os.getenv("DATABASE_NAME"),
                int(os.getenv("DATABASE_PORT")),
                i,
            )
            if dbHndlr_obj is not None and dbHndlr_obj.err == "":
                self.dbHndlrList.append(dbHndlr_obj)
        log.info("Initialized DB Pool")

    def select_one(self, qstr, *args):
        dbhndl_obj = None
        self.lock.acquire()
        try:
            for tmp_obj in self.dbHndlrList:
                if tmp_obj.isFree is True:
                    dbhndl_obj = tmp_obj
                    dbhndl_obj.isFree = False
                    # log.info("Found idle dbhandle id = %s",str(dbhndl_obj.id))
                    break
        except Exception as e:
            log.critical("Exception During Database selection=%s", str(e))
        self.lock.release()
        if dbhndl_obj is None:
            log.error("No dbhandle free....CANNOT PROCEED")
            return "False", None
        stat, rowset = dbhndl_obj.execute(qstr, "SELECT_ONE", *args)
        dbhndl_obj.isFree = True
        return stat, rowset

    def select(self, qstr, *args):
        dbhndl_obj = None
        self.lock.acquire()
        try:
            for tmp_obj in self.dbHndlrList:
                if tmp_obj.isFree is True:
                    dbhndl_obj = tmp_obj
                    dbhndl_obj.isFree = False
                    # log.info("Found idle dbhandle id = %s",str(dbhndl_obj.id))
                    break
        except Exception as e:
            log.critical("Exception During Database selection=%s", str(e))
        self.lock.release()
        if dbhndl_obj is None:
            log.error("No dbhandle free....CANNOT PROCEED")
            return "False", None
        stat, rowset = dbhndl_obj.execute(qstr, "SELECT", *args)
        dbhndl_obj.isFree = True
        return stat, rowset

    def update(self, qstr, *args):
        # stat,rowset = self.execute("SAVEPOINT aa",'savepoint')
        # stat,rowset = self.execute(qstr,'UPDATE')
        dbhndl_obj = None
        self.lock.acquire()
        try:
            for tmp_obj in self.dbHndlrList:
                if tmp_obj.isFree is True:
                    dbhndl_obj = tmp_obj
                    dbhndl_obj.isFree = False
                    # log.info("Found idle dbhandle id = %s",str(dbhndl_obj.id))
                    break
        except Exception as e:
            log.critical("Exception During free database handle selection=%s", str(e))
        self.lock.release()
        if dbhndl_obj is None:
            log.error("No dbhandle free....CANNOT PROCEED")
            return "False", None
        stat, rowset = dbhndl_obj.execute(qstr, "UPDATE", *args)
        dbhndl_obj.isFree = True
        return stat, rowset

    def delete(self, qstr, *args):
        # stat,rowset = self.execute("SAVEPOINT aa",'savepoint')
        # stat,rowset = self.execute(qstr,'DELETE')
        dbhndl_obj = None
        self.lock.acquire()
        try:
            for tmp_obj in self.dbHndlrList:
                if tmp_obj.isFree is True:
                    dbhndl_obj = tmp_obj
                    dbhndl_obj.isFree = False
                    # log.info("Found idle dbhandle id = %s",str(dbhndl_obj.id))
                    break
        except Exception as e:
            log.critical("Exception During Database selection=%s", str(e))
        self.lock.release()
        if dbhndl_obj is None:
            log.error("No dbhandle free....CANNOT PROCEED")
            return "False", None
        stat, rowset = dbhndl_obj.execute(qstr, "DELETE", args)
        dbhndl_obj.isFree = True
        return stat, rowset

    def insert(self, qstr, *args):
        dbhndl_obj = None
        self.lock.acquire()
        try:
            for tmp_obj in self.dbHndlrList:
                if tmp_obj.isFree is True:
                    dbhndl_obj = tmp_obj
                    dbhndl_obj.isFree = False
                    # log.info("Found idle dbhandle id = %s",str(dbhndl_obj.id))
                    break
        except Exception as e:
            log.critical("Exception During Database selection=%s", str(e))
        self.lock.release()
        if dbhndl_obj is None:
            log.error("No dbhandle free....CANNOT PROCEED")
            return "False", None
        try:
            stat, rowset, rowid = dbhndl_obj.execute(qstr, "INSERT", *args)
        except Exception:
            stat, rowset, rowid = False, None, -1
        finally:
            dbhndl_obj.isFree = True
        return stat, rowset, rowid

    def commit(self):
        return "True", "Commit"

    def close(self):
        for tmp_obj in self.dbHndlrList:
            tmp_obj.cursor.close()
            tmp_obj.conn.close()
            tmp_obj.isFree = False
