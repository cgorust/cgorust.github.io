class Converter {
  constructor() { 
    this.showdown();
    this.highlight();
    this.mermaid();
  }

  showdown() {
    const tagMap = {
      table: 'table table-striped',
    }
      
    const bindings = Object.keys(tagMap)
      .map(key => ({
        type: 'output',
        regex: new RegExp(`<${key}(.*)>`, 'g'),
        replace: `<${key} class="${tagMap[key]}" $1>`
    }));
    
    var converter = new showdown.Converter({
        tables: true 
        ,omitExtraWLInCodeBlocks: true
        ,emoji: true 
        ,noHeaderId: false
        ,parseImgDimensions: true
        ,simplifiedAutoLink: true
        ,literalMidWordUnderscores: true
        ,strikethrough: true
        ,tablesHeaderId: false
        ,ghCodeBlocks: true
        ,tasklists: true
        ,smoothLivePreview: true
        ,prefixHeaderId: false
        ,disableForced4SpacesIndentedSublists: false
        ,ghCompatibleHeaderId: true
        ,smartIndentationFix: false    
    });
    converter.setFlavor('github');
    var code_html = $('#word_content').text();
    code_html = converter.makeHtml(code_html);
    $("#word_content").html(code_html);
  }

  highlight() {
    document.querySelectorAll('pre code').forEach((block) => {
      hljs.highlightBlock(block);
    });
  }

  mermaid() {
    mermaid.initialize({startOnLoad: false});

    document.querySelectorAll('.mermaid').forEach((block) => {
      mermaid.render('theGraph', block.textContent.trim(), function(svgCode) {
          block.innerHTML = svgCode;
      });
    });  
  }
}	

export { Converter };

if (false) {
  let converter = new Converter();
}
