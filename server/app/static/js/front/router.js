define(['app','angular-ui-router'],function(app){
        app.config(['$stateProvider', '$urlRouterProvider',
            function($stateProvider, $urlRouterProvider) {
                $stateProvider.
                state('index', {
                    url:'/',
                    templateUrl: '/static/partials/front/index.html',
                    controller: 'indexCtr'
                }).
                state('post', {
                    url:'/post/{id:[0-9]+}',
                    templateUrl: '/static/partials/front/article.html',
                    controller: 'articleCtr'
                })
                // $locationProvider.html5Mode(true);
                $urlRouterProvider.otherwise('/');
            }
        ])
})
