define(['jquery',
        'base/js/events',
        'base/js/utils'],
function($, events, utils){
    function load_ipython_extension(){
        var diff_li = '<li class="dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown">Diff</a>' +
                            '<ul id="diff_menu" class="dropdown-menu">' +
                                '<li id="git_compare" class="dropdown-submenu"><a href="#">Git Compare</a>' +
                                    '<ul class="dropdown-menu">' +
                                        '<li><a href="#">Not in Git</a></li>' +
                                    '</ul>' +
                                '</li>' +
                            '</ul>' +
                        '</li>';
                        
        $("ul.navbar-nav").append(diff_li);
        
        var request_git_log = function(path) {
            var url = IPython.notebook.contents.api_url(path, 'gitlog');
            var settings = {
                type : "GET",
                cache: false,
                dataType: "json",
            };
            return utils.promising_ajax(url, settings);
        };
        
        var git_compare = function(commit){
            if (IPython.notebook.dirty){
                IPython.notebook.save_notebook().then(function() {
                    nbdiff(IPython.notebook.notebook_path, commit);
                });
            } else {
                nbdiff(IPython.notebook.notebook_path, commit);
            }
        }
        
        var nbdiff = function (path, path2) {
            var url;
            if (path2){
                url = IPython.notebook.contents.api_url(path, 'nbdiff', path2);
            } else {
                url = IPython.notebook.contents.api_url(path, 'nbdiff');
            }
            window.open(url, '_blank');
        };
        
        var load_git_log = function () {
            request_git_log(IPython.notebook.notebook_path).then(
                $.proxy(update_git_compare, this),
                function(error) {
                    events.trigger('load_git_log_failed.Notebook', error);
                }
            );
        };
        
        var update_git_compare = function(gitlog) {
            var ul = $("#git_compare").find("ul");
            ul.empty();
            if (!gitlog || gitlog.length === 0) {
                ul.append(
                    $("<li/>")
                    .addClass("disabled")
                    .append(
                        $("<a/>")
                        .text("Not in Git")
                    )
                );
                return;
            }
            
            var that = this;
            gitlog.map(function (commit) {
                var d = new Date(commit.last_modified);
                ul.append(
                    $("<li/>").append(
                        $("<a/>")
                        .attr("href", "#")
                        .text(moment(d).format("LLLL"))
                        .click(function () {
                            git_compare(commit.id);
                        })
                    )
                );
            });
        };
        
        load_git_log();
    }
    return {load_ipython_extension: load_ipython_extension};
}
)

