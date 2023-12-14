def call(Map config) {
	def stagesSkipped = config.stagesSkipped?:''
	def stagesToSkip = stagesSkipped.tokenize(',')
	def CMNodeName = config.CMNodeName ? config.CMNodeName : 'master'

	pipeline {
		agent {
			node config.nodeName
		}
		options {
			skipDefaultCheckout(true)
			timeout(time: config.timeOut, unit: 'HOURS')
			disableConcurrentBuilds()
			timestamps()
		}
		stages {
			stage('SetBuildName') {
				steps {
					script {
						currentBuild.displayName = config.bldDisplayName
					}
				}
			}
			stage('GetCode') {
				when {
					anyOf {
						expression { return !(stagesToSkip.contains('GetCode'))}
						expression { return config.containsKey('CustomStage_AfterGetCode')}
					}
				}
				steps {
					script {
						if(config.containsKey('GetCode')) {
							config.GetCode.call(config)
						} else if (!(stagesToSkip.contains('GetCode'))) {
							def repos = config.repoUrl?:""
							def repoList = repos.tokenize(',')
							def repoNames = config.repoName?:''
							def repoNameList=repoNames.tokenize(',')
							def repoLocations=config.repoLocation?:''
							def repoLocationList=repoLocations.tokenize(',')
							def repoBranches=config.repoBranch?:''
							def repoBranchList=repoBranches.tokenize(',')
							
							for (int i=0;i<repoList.size();i++) {
								def currentrepo=repoList.get(i)
								def currentrepoName=repoNameList.get(i)
								def currentrepoLocation=repoLocationList.get(i)
								def currentrepoBranch=repoBranchList.get(i)
								retry(3) {
									bat "echo current repo is ${currentrepo}"
									bat """
										IF EXIST "${currentrepoLocation}\\${currentrepoName}" (
											echo ${currentrepoLocation}\\${currentrepoName} already cloned
											CD "${currentrepoLocation}\\${currentrepoName}"
											echo clean workspace and pull
											git rev-parse --verify HEAD
											git reset --hard
											git clean -fdx
											git checkout ${currentrepoBranch} --
											git pull
										) ELSE (
											echo git clone ...
											IF NOT EXIST "${currentrepoLocation}" MD "${currentrepoLocation}"
											CD "${currentrepoLocation}"
											git clone -b ${currentrepoBranch} ${currentrepo} ${currentrepoName}
										)
									"""
								}
							}
						}

						if(config.containsKey('CustomStage_AfterGetCode')) {
							config.CustomStage_AfterGetCode.call(config)
						}
					}
				}
			}
			stage('RunSTEX') {
				when {
					anyOf {
						expression { return !(stagesToSkip.contains('RunSTEX'))}
						expression { return config.containsKey('CustomStage_AfterRunSTEX')}
					}
				}
				steps {
					script {
						if(config.containsKey('RunSTEX')) {
							config.RunSTEX.call(config)
						} else if (!(stagesToSkip.contains('RunSTEX'))) {
							bat """
								CD /D "${config.stexScriptPath}"
								call python "${config.stexScriptName}" ${config.stexScriptParameters}
								if %ERRORLEVEL% NEQ 0 EXIT
							"""
						}

						if(config.containsKey('CustomStage_AfterRunSTEX')) {
							config.CustomStage_AfterRunSTEX.call(config)
						}
					}
				}
			}
			stage('CIReport') {
				when {
					anyOf {
						expression { return !(stagesToSkip.contains('CIReport'))}
						expression { return config.containsKey('CustomStage_AfterCIReport')}
					}
				}
				steps {
					script {
						if(config.containsKey('CIReport')) {
							config.CIReport.call(config)
						} else if (!(stagesToSkip.contains('CIReport'))) {
							bat """
								CD /D "${config.reportScriptPath}"
								call "${config.reportScriptName}" ${config.reportScriptParameters}
								if %ERRORLEVEL% NEQ 0 EXIT
							"""
						}

						if(config.containsKey('CustomStage_AfterCIReport')) {
							config.CustomStage_AfterCIReport.call(config)
						}
					}
				}
			}
			stage('Post')
			{
				when {
					anyOf {
						expression { return !(stagesToSkip.contains('Post'))}
						expression { return config.containsKey('CustomStage_AfterPost')}
					}
				}
				steps {
					script {
						if(config.containsKey('Post')) {
							config.Post.call(config)
						} else if (!(stagesToSkip.contains('Post'))) {
							retry(5) {
								triggerRemoteJob job: 'Common/PutConsolidateReporttoPanzura',
								blockBuildUntilComplete: false,
								maxConn: 5, 
								parameters: """nodeName=${CMNodeName}\nbuildVersion=${config.buildVersion}\nBATResult=Passed\nreportName=${config.reportName}\nCIReportSourcePath=${config.CIReportSourcePath}\nCIReportTargetPath=${config.CIReportTargetPath}\nproduct=${config.productName}""",
								pollInterval: 20,
								useCrumbCache: false,
    					    	useJobInfoCache: false,
								remoteJenkinsName: 'CMJenkins',
								shouldNotFailBuild: true
							}
						}

						if(config.containsKey('CustomStage_AfterPost')) {
							config.CustomStage_AfterPost.call(config)
						}
					}
				}
			}
		}
		post('SendEmail') {
			success {
				script {
					def CIReportPath = config.CIReportTargetPathForEmail + '\\\\' + config.reportName
					if (stagesToSkip.contains('SendEmail')) {
						echo "BAT success, and skip send e-mail."
					} else {
						catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
							retry(5) {
								triggerRemoteJob job: 'Common/CreateEmailResultFile',
								blockBuildUntilComplete: false,
								maxConn: 5,
								parameters: """ProductName=${config.productName}\nFullVersion=${config.buildVersion}\nBuildPhase=BAT\nPhaseResult=SUCCESS\nAlwaysNotify=True\nCIReportPath=${CIReportPath}""",
								pollInterval: 20,
								useCrumbCache: false,
								useJobInfoCache: false,
								remoteJenkinsName: 'CMJenkins',
								shouldNotFailBuild: true
							}
						}
					}
				}
			}
			failure {
				script {
					def CIReportPath = config.CIReportTargetPathForEmail + '\\\\' + config.reportName
					if (stagesToSkip.contains('SendEmail')) {
						echo "BAT failure, and skip send e-mail."
					} else {
						catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
							triggerRemoteJob job: 'Common/CreateEmailResultFile',
							blockBuildUntilComplete: false,
							maxConn: 5, 
							parameters: """ProductName=${config.productName}\nFullVersion=${config.buildVersion}\nBuildPhase=BAT\nPhaseResult=FAILURE\nAlwaysNotify=True\nCIReportPath=${CIReportPath}""",
							pollInterval: 20,
							useCrumbCache: false,
    					    useJobInfoCache: false,
							remoteJenkinsName: 'CMJenkins',
							shouldNotFailBuild: true
						}
					}
				}
			}
		}
	}
}
