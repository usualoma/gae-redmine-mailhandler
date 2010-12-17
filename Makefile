TESTS = \
	tests

TEST_OPTIONS = \
	--with-doctest
#TEST_OPTIONS +=	--with-gae
#TEST_OPTIONS +=	--nocapture
#TEST_OPTIONS +=	--nologcapture
#TEST_OPTIONS +=	-v

default: all 

all:
	@echo "Nothing to do"

test:
	@(nosetests $(TEST_OPTIONS) $(TESTS))

testxml:
	@(nosetests $(TEST_OPTIONS) --with-xunit $(TESTS) )

profile:
	@(nosetests --with-profile --profile-stats-file=nose.prof $(TESTS)) 
	@(python -c "import hotshot.stats ; stats = hotshot.stats.load('nose.prof') ; stats.sort_stats('time', 'calls') ; stats.print_stats(20)")

coverage:
	@(nosetests --with-coverage $(TESTS)) 

clean:
	find . -name '*.pyc' -exec rm '{}' ';'
