define(['app','services'], function(app) {
    app.controller('indexCtr', ['$scope', 'getList',
        function($scope, getList) {
            getList('post', 1, 5).success(function(data) {
                $scope.postList = data;
            })
        }
    ]).
    controller('articleCtr', ['$scope', '$stateParams', '$sce', 'Post',
        function($scope, $stateParams, $sce, Post) {
            var id = $stateParams.id;
            Post.get({
                id: id
            }, function(d) {
                d.content = $sce.trustAsHtml(d.content);
                $scope.post = d;
            })

        }
    ])

})