dev = ex
all: 
%-yaml : %.xml
	xsltproc $(dev)/to$(dev).xsl $< > ${@:%-yaml=%}.yaml
%-xml : src/%_config.xml
	xsltproc $(dev)/from$(dev).xsl $< > ${@:%-xml=%}.xml
% : %.yaml
	ansible-playbook $(dev)/$(dev)_playbook.yaml -e fname=../$@ -e @$<

clean:
	rm *.xml *.yaml *.txt

src/hp_config.xml : src/HP_config.txt
	php hp/toxml.php $< > $@
