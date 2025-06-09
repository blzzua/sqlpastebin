        (function(){
            var processFiles = function (event) {
                event.stopPropagation();
                event.preventDefault();
                removeDropZoneClass();

                // FileList object of File objects
                var files = event.dataTransfer.files;
                var output = [];
                for (var i = 0, f; f = files[i]; i++) {
                    var rdr = new FileReader();
		    //rdr.readAsText(f, 'UTF-8');
                    // closure to capture file info
                    rdr.onloadend = (function(file, index) {
                        return function(e) {
			    var xhttp = new XMLHttpRequest();	
                            var dataUri = e.target.result,
                                base64 = dataUri.substr(dataUri.indexOf(',') + 1),
                                textarea, image, figcaption;
//				console.log(base64);
//                            textarea = ['<textarea onfocus="this.select()">', base64, '</textarea>'].join('');
//			    alert(encodeURIComponent(atob(base64)));
                            if (file.type.match('image.*')) {
                                if (dataUri.length > 32768) {
                                    figcaption = '<figcaption>In IE8, data URIs cannot be larger than 32,768 characters.</figcaption>';
                                }
                                image = ['<figure><img class="thumb" src="', dataUri, '" title="', file.name, '"/>',
                                    figcaption, '</figure>'].join('');

				var doc_href = 'none';
				xhttp.onreadystatechange = function() {
				    if (xhttp.readyState == 4 && xhttp.status == 200) {
					var doc_id = JSON.parse(xhttp.responseText).key;
					var doc_url = [ window.location.href,'?i=',doc_id].join('');
                        		textarea = ['<div class="textarea"><dt><text>Your Link</text></dt><dt><input readonly="" onfocus="this.select()" value="', doc_url, '" type="text"></dt></div>'].join('');

                            document.getElementById(['file_', index + 1].join('')).innerHTML += [textarea].join('');
				    };
				}
				xhttp.open("POST", "/documents", true);
				xhttp.send(base64);
                            } else {
                        	document.getElementById('drop_zone').setAttribute('class', 'highlight')
                        	document.getElementById('drop_zone').innerHTML = 'Use <a href="/">editor</a> for non-image files !!!';
                        	highlightDropZone;
//                        	sleep(2000);
				setTimeout(function() { document.getElementById('drop_zone').removeAttribute('class');document.getElementById('drop_zone').innerHTML = 'Drop images here or open an <a href="/">editor</a>'; }, 1000);
				}

                        
                        };
                    })(f, i);

                    // read file as data URI
//                    output.push(loadEvent.target.result);
                    rdr.readAsDataURL(f);
                    if (f.type.match('image.*')) {
                    var data = ['<ol id="file_', i + 1, '"><h3>Name: ', f.name, '</h3><dl>',
                        '<dt>Type</dt><dd>', f.type || 'n/a', '</dd>',
                        '<dt>Size</dt><dd>', f.size, ' bytes</dd>',
                        '<dt>Last Modified</dt><dd>', f.lastModifiedDate ? f.lastModifiedDate.toDateString() : 'n/a', '</dd>',
                        '</dl></ol>'].join('');

                    output.push(data); 
                    rdr='';
                    }
                }
                if (files.length) {
                    document.getElementById('list').innerHTML = '<ol>' + output.join('') + '</ol>';
                }
            };

            var highlightDropZone = function (e) {
                e.stopPropagation();
                e.preventDefault();
                document.getElementById('drop_zone').setAttribute('class', 'highlight');
            }

            var removeDropZoneClass = function () {
                document.getElementById('drop_zone').removeAttribute('class');
            }
	    var sleep = function (milliseconds) {
	      var start = new Date().getTime();
	        for (var i = 0; i < 1e7; i++) {
	            if ((new Date().getTime() - start) > milliseconds){
	                  break;
	          }
	        }
	    }

	    var QueryString = function () {
	      var query_string = {};
	      var query = window.location.search.substring(1);
	      var vars = query.split("&");
	      for (var i=0;i<vars.length;i++) {
	    var pair = vars[i].split("=");
	        if (typeof query_string[pair[0]] === "undefined") {
	          query_string[pair[0]] = decodeURIComponent(pair[1]);
	        } else if (typeof query_string[pair[0]] === "string") {
	          var arr = [ query_string[pair[0]],decodeURIComponent(pair[1]) ];
	          query_string[pair[0]] = arr;
	        } else {
	      query_string[pair[0]].push(decodeURIComponent(pair[1]));
	        }
	      } 
	        return query_string;
	    }();

            // add event listeners if File API is supported

        
	    var dropZone = document.getElementById('drop_zone');
            if (window.File && window.FileReader && window.FileList && window.Blob) {
                dropZone.addEventListener('drop', processFiles, false);
                dropZone.addEventListener('dragover', highlightDropZone, false);
                dropZone.addEventListener('dragenter', highlightDropZone, false);
                dropZone.addEventListener('dragleave', removeDropZoneClass, false);
                dropZone.innerHTML = 'Drop images here or open an <a href="/">editor</a>';
            } else {
                dropZone.innerHTML = 'The Image APIs are not fully supported in this browser, try paste your text in <a href="/">editor</a>';
                dropZone.className = 'highlight';
            }

            // change doc element class to show JS support
            var docEl = document.documentElement;
            docEl.className = docEl.className.replace('no-', '');
	    if (typeof QueryString.i !== 'undefined') {

        	document.body.innerHTML = '';
	    var xhttp = new XMLHttpRequest();

				xhttp.onreadystatechange = function() {
				    if (xhttp.readyState == 4 && xhttp.status == 404) {
					    window.location.href = "/img";
				    } else if (xhttp.readyState == 4 && xhttp.status == 200) {
					var doc_url = ['<img src="data:image/gif;base64,',xhttp.responseText,'"/>'].join('');
					doc_href = ['<a href="'+doc_url+'">',doc_url,'</a>'].join('');
		                        document.body.innerHTML += ['<h1><a href="/img" class="logo" alt="Image Drop"></a></h1>',doc_url].join('');
				    }

				};
				doc_uri=['/raw/',QueryString.i].join('');
				xhttp.open("GET", doc_uri, true);
//				xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
				xhttp.send();
	    }
        })();
