from script_enhancement import isDiskOverUsage

def test_overThreshold():
    assert isDiskOverUsage(90) is True
    assert isDiskOverUsage(100, 50) is True

def test_belowThreshold():
    assert isDiskOverUsage(50) is False
    assert isDiskOverUsage(20, 50) is False

def test_edgeCase():
    assert isDiskOverUsage(79) is False
    assert isDiskOverUsage(80) is False
    assert isDiskOverUsage(81) is True