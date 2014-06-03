var twapp = angular.module("tw_app", ['ngRoute', 'twAppServices','n3-charts.linechart']);


twapp.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $routeProvider.when("/", {templateUrl: '/templates/twapp.tpl', controller: "mainController"});
        $routeProvider.when("/all", {templateUrl: '/templates/all.tpl', controller: "allController"});
        $routeProvider.when("/single", {templateUrl: '/templates/single.tpl', controller: "singleController"});
        $routeProvider.when("/chart", {templateUrl: '/templates/chart.tpl', controller: "chartController"});
}]);
