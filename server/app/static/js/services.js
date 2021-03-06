define(['angular','angular-resource'], function(angular) {
    var myService = angular.module('myService', ['ngResource']);
    myService.
    factory('getList', ['$http', function($http) {
        return function(listType, page, per_page) {
            return $http.get("/" + listType + "/list/" + page + "/" + per_page)
        };
    }]).
    factory('Post', ['$resource', 'Auth', function($resource, Auth) {
        return $resource("/app/post/:id", {
            id: '@id'
        }, {
            'update': {
                method: 'PUT',
                headers: {
                    'Auth': Auth.getToken()
                }
            },
            'get': {
                method: 'GET'
            },
            'delete': {
                method: "DELETE",
                headers: {
                    'Auth': Auth.getToken()
                }
            }
        })
    }]).
    factory('Posts', ['$resource', 'Auth', function($resource, Auth) {
        return $resource("/app/posts", {}, {
            'save': {
                method: 'POST',
                headers: {
                    'Auth': Auth.getToken()
                }
            }
        })
    }]).
    factory('Users', ['$resource', function($resource) {
        return $resource("/users")
    }]).
    service('Auth', ['$http', function($http) {
        this.authToken = {};
        this.getToken = function() {
            return this.authToken["token"];
        }
        this.setToken = function(value) {
            this.authToken["token"] = value;
        }
        this.removeToken = function(value) {
            this.authToken["token"] = '';
        }

    }])
})