toIgnoreRebase={
    "cccb4d78af5d60c40ac956ec14e252e58586950f",
    "0f9107917d964323cfc2d7ca85dafb6bef345d47",
    "cc38f4484eaf24fd95b66262ddb4c614ac208a00",
    "0c35cf66da28e7c7dacd66f73fb57a13ab650c74",
    "3775cfd4123fcaa50a74736dc34a1c223e6e6852",
    "6d72a9c6a2192177c4f2f197f067f8174c172b71",
    "8209662ef0a32a9fded1442aa6bdc2e21ea74a3e",
    "24daaee972b823159fa605994bd5be774614e91c",
    "d5317ee6742b057c57408b54b70522b2b88e0a70",
    "0c35cf66da28e7c7dacd66f73fb57a13ab650c74",
    "b4bb62a11b7a4c536c719027e3549505f1c97f54",
    "fbb0fb41a252bd3d0e2274f7364b95f3c194c256",
    "e8c35c5997c42681aa4bb30a6d97b53394df49da",
    "55fd9ebaf1bb341148a41890336c5921ef225a30",
    "534ce6221e4d3f2ab49fcfd32bb061be4be0de2b",
    "055e063184bb4ede8518ec42dc7ca605b07b0b61",
    "18f1d263653e62faaafcc283b5f174a31bee1b5a",
    "f9c05b080d338b59e09c7bdc2ca76e74f6a5b648",
    "571da4458b99db8929feae126d847822945661a2",
    "540cb1bc8f8bcf07190c7fb5c5e18a04cbd9e307",
    "0aabb6cda66c63e7a8ac7013fa2edd7bc148d40a",
    "0c35cf66da28e7c7dacd66f73fb57a13ab650c74",
    "3775cfd4123fcaa50a74736dc34a1c223e6e6852",
    "8209662ef0a32a9fded1442aa6bdc2e21ea74a3e",
    "607b90f9f947ed24445e5b5adda66ab63261260b",
    "00780c0bca5d07868c15e72d4e10cff659b2f507",
}
pairs = [# We don't rebase commented, in order to verify which
    # comments are related to something which has changed.
    ("elmes/master", "intToConstant"),

    ("intToConstant", "factorized"),
    ("factorized", "commented"),
    ("commented", "baseFork"),

    # Add-ons dealing with the long data base checking process
    ("baseFork", "explodeFixIntegrity"), # hard to test. Does not raise an error while checking.
    ("explodeFixIntegrity", "usableEmptyCards"), # debugged
    ("explodeFixIntegrity", "correctNewDue"), # Hard to debug
    ("explodeFixIntegrity", "quickerChangeModel"),# updated
    ("quickerChangeModel", "explainDeletion"),

    # Add-ons dealing with card generation
    ("quickerChangeModel", "bigChangeModel"),
    ("consistentCardGeneration", "bigChangeModel"),

    # Add-ons dealing with browser
    ("baseFork", "exportBrowser"), # works
    ("baseFork", "browserRefresh"), #tested
    ## Browser columns' content
    ("baseFork", "browserColumns"), #tested
    ("browserColumns", "advancedBrowser"), #tested
    ("browserColumns", "browserForNote"), #tested
    ("browserColumns", "minutesInBrowser"), #tested
    ("minutesInBrowser", "advancedBrowser"), #tested
    ("browserColumns", "browserExtraColumns"),
    ("browserForNote", "advancedBrowser"),
    ("browserExtraColumns", "advancedBrowser"),

    ("baseFork", "addedToday"), # Debugged
    ("baseFork", "allowEmptyFirstField"),
    ("baseFork", "batchEdit"),#works
    ("baseFork", "changeDeckPrefix"),# works
    ("baseFork", "changeTypeOfNoteWithoutSync"), # to test
    ("baseFork", "colors"),
    ("colors", "deckBrowserEnhanced"),
    ("baseFork", "compileLatex"),#works
    ("baseFork", "considerNameWhenChangingTypeOfANote"), # debugged
    ("baseFork", "copyNote"),# Debugged
    ("baseFork", "emptyNewCard"), # works
    ("baseFork", "explainDeletion"), # debugged
    ("baseFork", "forkCommented"), # Only documentation change
    ("baseFork", "removeMapTo"),
    ("baseFork", "keepFieldsInAddCard"),# Debugged
    ("baseFork", "keepNoteWithoutCards"), #Debugged
    ("baseFork", "limitCardsNumberCountingEverything"),
    ("baseFork", "longTermBackup"),
    ("baseFork", "newlineJson"),# debugged
    ("baseFork", "multipleWindow"),# debugged, with todo
    ("baseFork", "postponeDays"),# debugged
    ("baseFork", "quickerRenderingOfQA"), # works
    ("baseFork", "tagMissingMedia"),# debugged, with todo
    ("baseFork", "consistentCardGeneration"),
    #("baseFork", "keepMoreFiles"),
    ("quickerChangeModel", "multiColumnEditor"), #debugged
    ("multiColumnEditor", "frozenFields"), # debugged
]

parents = {p[0] for p in pairs}
children = [p[1] for p in pairs]
leaves = [child for child in children if child not in parents]
