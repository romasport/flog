define(['app'],function(app){
    app.directive('colorful',function() {
        return {
            restrict: "AE",
            scope: {},
            link: function(scope, elem, attrs) {
                if (attrs.colorful){
                        flat = "flat_border_" + Math.ceil((18 * Math.random()));
                         elem.addClass(flat)
                } else {
                    flat = "flat_" + Math.ceil((18 * Math.random()));
                    flat_hover="flat_hover_"+Math.ceil((18 * Math.random()));
                    elem.addClass(flat+" "+flat_hover)
                }
            }
        }
    })
    
})