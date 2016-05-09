'use strict';

angular.module('NoMsg.messagegetall', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/messagegetall', {
    templateUrl: 'messagegetall/messagegetall.html',
    controller: 'MessageGetAllCtrl'
  });
}])
.controller('MessageGetAllCtrl', function($scope, $http){

    // If the submit button is pressed.
    $scope.submit = function() {

        var user2fa = $scope.input2fa;
        var username = $scope.inputUsername;

        // @app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['GET'])
        var url = "http://127.0.0.1:5000/user/"+username+"/2fa/"+user2fa+"/message/";
        $http.get(url)
        .then(function(response){
            var responseData = response.data;

            // If response was error,
            // display the text rather than displaying the table.
            if(responseData.indexOf("Error:") == -1){
                $scope.responseText = "";
                $scope.responseData = responseData;
            } else {
                $scope.responseText = responseData;
            }
        });
    };
});