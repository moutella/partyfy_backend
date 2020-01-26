jQuery(document).ready(function () {
    var tracks = []

    function create_searchs() {
        console.log(jQuery("#song_name").val());
        jQuery.ajax({
            url: 'https://api.spotify.com/v1/search?type=track&q=' + jQuery("#song_name").val(),
            headers: {
                'Authorization': 'Bearer ' + data.token
            },
            success: function (response) {
                tracks = []
                for (var track in response.tracks.items) {
                    var track_data = {
                        label: response.tracks.items[track].name,
                        value: response.tracks.items[track].uri,
                        cover: response.tracks.items[track].album.images[0].url,
                        album: response.tracks.items[track].album.name,
                        artist: response.tracks.items[track].album.artists[0].name
                    }
                    tracks.push(track_data);
                }
            },
            complete: function () {
                updateAutoComplete();
                jQuery("#song_name").autocomplete("search", jQuery("#song_name").val());
            }
        });
    }

    function addTextAreaCallback(textArea, callback, delay) {
        var timer = null;
        textArea.onkeypress = function () {
            if (timer) {
                window.clearTimeout(timer);
            }
            timer = window.setTimeout(function () {
                timer = null;
                callback();
            }, delay);
        };
        textArea = null;
    }

    addTextAreaCallback(document.getElementById("song_name"), create_searchs, 350);

    function updateAutoComplete() {
        jQuery("#song_name").autocomplete({
                minLength: 0,
                source: tracks,
                focus: function (event, ui) {
                    jQuery("#song_name").val(ui.item.label);
                    return false;
                },
                select: function (event, ui) {
                    jQuery("#song_name").val(ui.item.label);
                    jQuery("#request_song_uri").val(ui.item.value);
                    jQuery("#request_song_form").submit();
                    return false;
                }
            })
            .autocomplete("instance")._renderItem = function (ul, item) {
                console.log(item);
                return $("<li>")
                    .append("<div class='row'>" +
                        "<div class='col-2'><img style='width: 100%'src=" +
                        item.cover +
                        "></img></div>" +
                        item.label +
                        "<br>" +
                        item.artist + "</div>"
                    )
                    .appendTo(ul);
            };
        jQuery.ui.autocomplete.prototype._resizeMenu = function () {
            var ul = this.menu.element;
            ul.outerWidth(this.element.outerWidth());
        }
    }
});