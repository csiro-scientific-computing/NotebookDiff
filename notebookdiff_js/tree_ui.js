define(['jquery',
        'base/js/events',
        'base/js/utils'],
function($, events, utils){
    var nbdiff = function (path, path2) {
        var url = IPython.notebook_list.contents.api_url(path, 'nbdiff', path2);
        window.open(url, '_blank');
    };
    
    //Add diff button
    var button_diff = $('<button title="Compare selected" class="btn btn-default btn-xs">Diff</button>');
    button_diff.click(function(){
        var selected = IPython.notebook_list.selected;
        var path1 = selected[0].path;
        var path2 = selected[1].path;
        nbdiff(path1, path2);
    });
    var old_selection_changed = IPython.NotebookList.prototype._selection_changed;
    $('#notebook_toolbar .dynamic-buttons').append(button_diff);
    
    IPython.NotebookList.prototype._selection_changed = function(){
        //call the original function
        old_selection_changed.call(this);
        
        //Show or hide diff button
        var selected = IPython.notebook_list.selected;
        var has_directory = false;
        var has_file = false;
        $('.list_item :checked').each(function(index, item) {
            var parent = $(item).parent().parent();

            if (parent.find('.upload_button').length === 0 && parent.data('path') !== '') {
                // Set flags according to what is selected.  Flags are later
                // used to decide which action buttons are visible.
                has_file = has_file || parent.data('type') == 'file';
                has_directory = has_directory || parent.data('type') == 'directory';    
            }
        });
        
        if (selected.length == 2 && !(has_file || has_directory)){
            button_diff.css('display', 'inline-block');
        } else {
            button_diff.css('display', 'none');
        }
    };
});

