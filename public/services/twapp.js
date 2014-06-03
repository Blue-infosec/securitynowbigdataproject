var gtw = angular.module('twAppServices', ['ngResource']);

gtw.service('gettwapp', ['$resource', function () {

    console.log("SERVICE INITIALIZED");

    this.fullSet = function (limit, skip, cb) {
        skip == 0 ? skip = 1 : skip = skip;
        limit == 0 ? limit = 1 : limit = limit;
        $.get("/fullset/" + limit + "/" + skip + "", function (data) {
            cb(data);
        });
    }

    this.episode = function (id, cb) {
        $.get("/episode/" + id, function (data) {
            cb(data);
        });
    }

    this.search = function (id, cb) {
        $.get("/search/" + id, function (data) {
            cb(data);
        });
    }

    this.happy = function (id, cb) {
        $.get("/whoshappy/" + id, function (data) {
            cb(data);
        });
    }

    this.mad = function (id, cb) {
        $.get("/whosmad/" + id, function (data) {
            cb(data);
        });
    }

}]);