var gtw = angular.module('twAppServices', ['ngResource']);

    gtw.service('gettwapp', ['$resource', function () {

        console.log("SERVICE INITIALIZED")

            this.fullSet = function (cb) {
                $.get("/fullset", function (data) {
                    cb(data);
                });
            }

            this.pagedSet = function (id, cb) {
                $.get("/pagedSet/"+id, function (data) {
                    cb(data);
                });
            }

            this.episode = function (id, cb) {
                $.get("/episode/"+id, function (data) {
                    cb(data);
                });
            }

            this.search = function (id, cb) {
                $.get("/search/"+id, function (data) {
                    cb(data);
                });
            }

    }]);