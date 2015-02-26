define(['angular', 'angular-resource', 'angular-animate', 'angular-sanitize', 'angular-ui-router','services'], function(angular) {
    return angular.module('time', ['ui.router', 'ngResource', 'ngAnimate', 'myService', 'ngSanitize']);
})