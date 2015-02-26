define(['app','services','ngDialog','angular-ui-router'],function(app){
    app.
    controller('postListCtr', ['$scope', 'getList', function($scope, getList) {
        getList('article', 1, 10).success(function(data) {
            $scope.dataList = data;
        })
    }]).
    controller('dashCtr', ['$scope', '$window','$http','ngDialog', 'Auth',function($scope, $window,$http,ngDialog,Auth) {
        $scope.logout = function() {
            ngDialog.openConfirm({ //popup dialog to confire some action
                template: 'logout',
                className: 'ngdialog-theme-default'
            }).then(function(value) { // do action
                $window.sessionStorage['token']="";
                Auth.removeToken();
                setTimeout(function(){
                    $window.location.href="/";
                },1000);
            }, function(reason) { // cancle action
                console.log(reason);
            });
        }
    }]).
    controller('postActionCtr', ['$scope', '$location', 'Posts', 'Post', '$stateParams', 'Categorys', 'Category', 'ngDialog', function($scope, $location, Posts, Post, $stateParams, Categorys, Category, ngDialog) {
        var id = $stateParams.id
        $scope.formData = {};
        $scope.postCategory = {};
        /*先处理category*/
        Categorys.query(function(d) {
            $scope.categoryList = d;
        })
        $scope.createCategory = ""; //新建category的数据model
        $scope.postCategory.data = []; //要提交的cetegory的数据model
        function resetData(ob) {
            for (var i in ob) {
                if (typeof(ob[i]) == 'string') {
                    ob[i] = "";
                    continue;
                }
                if (ob[i] instanceof Array) {
                    ob[i] = [];
                    continue;
                }
                if (typeof(ob[i]) == "object") {
                    ob[i] = {};
                }
            }
        }

        function notify(info) {
            ngDialog.open({
                template: 'notify',
                data: {
                    action: info
                }
            })
        }
        $scope.categoryAdd = function() {
            var category = new Categorys();
            category.name = $scope.createCategory;
            category.$save(function() { //提交分类
                Category.get({
                    id: $scope.createCategory
                }, function(d) { //获取提交分类的id
                    $scope.categoryList.push({
                            'id': d.id,
                            'name': d.name
                        }) //更新到scope作用域中
                })
            })
        }

        if (id) {
            /*modify post*/
            $scope.action = "MODIFY POST";
            Post.get({
                id: id
            }, function(d) {
                $scope.formData = d;
                /*set exist category*/
                for (var i = 0; i < d.category.length; i++) {
                    $scope.postCategory.data.push(d.category[i].id)
                }

            })

            $scope.postAction = function() {
                var post = new Post();
                post.title = $scope.formData.title;
                post.content = $scope.formData.content;
                post.category = $scope.postCategory.data;
                if (!post.category.length) {
                    notify("分类必须填写");
                } else {
                    post.$update({
                        id: id
                    }, function() {
                        notify("文章更新成功");
                        $scope.$on("ngDialog.closed", function() {
                            $scope.$apply(function() {
                                $location.path("/post/list");
                            })
                        })
                    });
                }
            }

        } else {
            /*create post*/
            $scope.action = "NEW POST";
            $scope.postAction = function() {
                var post = new Posts();
                post.title = $scope.formData.title;
                post.content = $scope.formData.content;
                post.category = $scope.postCategory.data;
                if (!post.category.length) {
                    notify("分类必须填写")
                } else {
                    post.$save({}, function(success) { //post success  callback
                        resetData($scope.formData);
                        $scope.postCategory.data = [];
                        $scope.post.$setPristine();
                        notify("文章添加成功")
                    }, function(error) { //post error callback
                        notify("文章添加失败: " + error.statusText)
                    });
                }
            }
        }
    }]).
    controller('login', ['$scope', '$window', '$http', 'Auth', function($scope, $window, $http, Auth) {
        $scope.loginData = {};
        $scope.signIn = function() {
            $scope.loading = true;
            $http.post('/users', {
                username: $scope.loginData.username,
                passwd: $scope.loginData.passwd
            }).then(function(d) {
                $scope.loading = false;
                if (d.data.token) {
                    $scope.notice = "You are login in";
                    $scope.dash = true;
                    var token = d.data.token;
                    Auth.setToken(token);
                    $window.sessionStorage["token"] = token;
                } else {
                    $scope.notice = "login in error,try again";
                    $scope.dash = false;
                }
            }, function(error) {
                console.log(error)
            })

        }

    }])
})