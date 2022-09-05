class Util {
	static async getJSON(file) {
	  let val;
	  await $.getJSON(file, function(data) {
	    val = data;
	  })
	  .fail(function() {
	    console.log( "getJSON error! file:" + file);
	  })
	  return val;
	}
}

export { Util };

if (false) {
	Util.getJSON("/client/config/config.json").then(data => { 
		console.log(data);
  });
}
