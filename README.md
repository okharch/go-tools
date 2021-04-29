# go-tools
Various tools to automate go development

## go-get-files.pl
It uses ```go list -n -v -a -json -deps``` to generate json with array of all dependencies for current build.
Then it parses that json and lists GoFiles for each module.
It is useful to operate over all of the go files in project.
