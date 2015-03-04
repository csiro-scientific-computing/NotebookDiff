// leave at least 2 line with only a star on it below, or doc generation fails
/**
 *
 *
 */

require([
    'base/js/events'
], function(events) {
    events.on('app_initialized.DashboardApp', function(){
        require(['../../nbextensions/notebookdiff_js/tree_ui.js']);
    });
});