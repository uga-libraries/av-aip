<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
	xmlns:premis="http://www.loc.gov/premis/v3"
	xmlns:dc="http://purl.org/dc/terms/"
	xpath-default-namespace="https://mediaarea.net/mediainfo">
	<xsl:output method="xml" indent="yes"/>
	
	<!--This stylesheet creates preservation.xml from MediaInfo XML output.-->
	<!--It is used as part of the workflow for making AIPs.-->

	<!--TODO: Replace XPath for outdated versions of MediaInfo in RBRL-specific parts of code.-->
	
	
	<!-- *************************************************************************************************************** -->
	<!-- **************************************** OVERALL STRUCTURE OF MASTER.XML ************************************** -->
	<!-- *************************************************************************************************************** -->
	
	<xsl:template match="/">
		<preservation>
			<xsl:call-template name="aip-title"/>
			<dc:rights>http://rightsstatements.org/vocab/InC/1.0/</dc:rights>
			<aip>
				<premis:object>
					<xsl:call-template name="aip-id"/>
					<xsl:call-template name="aip-version"/>
					<xsl:call-template name="object-category"/>
					<premis:objectCharacteristics>
						<xsl:call-template name="aip-size"/>
						<xsl:call-template name="aip-unique-formats"/>
					</premis:objectCharacteristics>
					<xsl:call-template name="relationship-collection"/>
				</premis:object>
			</aip>
			<xsl:if test="$file-count > 1">
				<filelist><xsl:apply-templates select="//track[@type='General']"/></filelist>
			</xsl:if>
		</preservation>
	</xsl:template>
	
	
	<!-- *************************************************************************************************************** -->
	<!-- ************************************************* GLOBAL VARIABLES ******************************************** -->
	<!-- *************************************************************************************************************** -->
	
	<!--Value of parameter is given to the stylesheet by the command to run the stylesheet.-->
	<xsl:param name="department" required="yes"/>
	
	<!--Use this for the parameter instead to run the stylesheet with an XML editor.-->
	<!--<xsl:param name="department">bmac</xsl:param>-->
	
	<xsl:variable name="uri">
		<xsl:if test="$department = 'bmac'">http://archive.libs.uga.edu/bmac</xsl:if>
		<xsl:if test="$department = 'rbrl'">http://archive.libs.uga.edu/russell</xsl:if>
	</xsl:variable>
	
	<xsl:variable name="collection-id">
		<xsl:if test="$department = 'bmac'">
			<xsl:choose>
				<xsl:when test="matches($filename, 'wsbn')">wsbn</xsl:when>
				<xsl:when test="matches($filename, 'walb')">walb</xsl:when>
				<xsl:when test="matches($filename, 'FM')">wsb-video</xsl:when>
				<xsl:when test="matches($filename, '^\d{5,6}')">peabody</xsl:when>
				<xsl:when test="matches($filename, '^bmac_\d{5,6}')">peabody</xsl:when>
				<!--This is for DPX that aren't Peabody.-->
				<xsl:when test="matches($filename, '^bmac_')">
					<xsl:analyze-string select="$filename" regex="^bmac_([a-z0-9-]+)">
						<xsl:matching-substring><xsl:value-of select="regex-group(1)"/></xsl:matching-substring>
					</xsl:analyze-string>
				</xsl:when>
				<xsl:otherwise>
					<xsl:analyze-string select="$filename" regex="([\w_-]+)_">
						<xsl:matching-substring><xsl:value-of select="regex-group(1)"/></xsl:matching-substring>
					</xsl:analyze-string>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
		<xsl:if test="$department = 'rbrl'">
			<xsl:analyze-string select="$aip-filepath/FileName" regex="(rbrl\d{{2,4}})">
				<xsl:matching-substring><xsl:sequence select="regex-group(1)"/></xsl:matching-substring>
			</xsl:analyze-string>
		</xsl:if>
	</xsl:variable>
	
	<xsl:variable name="aip-id">
		<xsl:if test="$department = 'bmac'">
			<xsl:choose>
				<xsl:when test="//FileExtension = 'dpx'">
					<xsl:if test="/MediaInfo/media[1]/track[@type='General']/CompleteName_Last[contains[bmac_]]">
						<xsl:text>bmac_</xsl:text>
					</xsl:if>
					<xsl:value-of select="$filename"/>
				</xsl:when>
				<!--ADDED TO AVOID DOUBLE BMACS-->
				<xsl:otherwise>
					<xsl:if test="not(starts-with($filename, 'bmac_'))">bmac_</xsl:if>
					<xsl:value-of select="$filename"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
		<!--This is getting an error in Saxon: Evaluation will always throw a dynamic error. No expression before quantifier.-->
		<!--<xsl:if test="$department = 'rbrl'">
			<xsl:analyze-string select="$aip-filepath/FolderName" regex="(rbrl\d{{3}}\w{{2,5}}-\w.**)/objects">
				<xsl:matching-substring><xsl:value-of select="regex-group(1)"/></xsl:matching-substring>
			</xsl:analyze-string>
			<xsl:choose>
				<xsl:when test="//FileExtension[contains(., 'xml')] or //FileExtension[contains(., 'pdf')] or //FileExtension[contains(., 'doc')]">
					<xsl:text>_metadata</xsl:text>
				</xsl:when>
				<xsl:when test="//FileExtension[contains(., 'mov')] or //FileExtension[contains(., 'wav')] or //FileExtension[contains(., 'mp3')] or //FileExtension[contains(., 'dv')]">
					<xsl:text>_media</xsl:text>
				</xsl:when>
			</xsl:choose>
		</xsl:if>-->
	</xsl:variable>
	
	<!--BMAC uses this to get collection-id and aip-id-->
	<xsl:variable name="filename">
		<xsl:choose>
			<xsl:when test="//FileExtension='dpx'">
				<xsl:analyze-string select="/MediaInfo/media[1]/@ref" regex="^([\w_-]+)/objects">
					<xsl:matching-substring><xsl:value-of select="regex-group(1)"/></xsl:matching-substring>
				</xsl:analyze-string>
			</xsl:when>
			<xsl:otherwise>
				<xsl:analyze-string select="/MediaInfo/media[1]/@ref" regex="([\w_-]+)\.[mov|mxf|mkv|wav]">
					<xsl:matching-substring><xsl:value-of select="regex-group(1)"/></xsl:matching-substring>
				</xsl:analyze-string>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	
	<!--Long filepath that is frequently used by RBRL-->
	<xsl:variable name="aip-filepath" select="/MediaInfo/File[1]/track[@type='General'][1]"></xsl:variable>
	
	<!--File count for when single and multiple file AIPs are treated differently-->
	<xsl:variable name="file-count">
		<xsl:value-of select="count(/MediaInfo/media)"/>
	</xsl:variable>
	
	
	<!-- *************************************************************************************************************** -->
	<!-- ************************************************* AIP TEMPLATES *********************************************** -->
	<!-- *************************************************************************************************************** -->
	
	<xsl:template name="aip-title">
		<xsl:if test="$department = 'bmac'">
			<dc:title><xsl:value-of select="$aip-id"/></dc:title>
		</xsl:if>
		<!--This is getting an error in Saxon: Evaluation will always throw a dynamic error. No expression before quantifier.-->
		<!--<xsl:if test="$department = 'rbrl'">
			<dc:title>
				RBRL QUESTION: is this the right order for handling possible rule conflicts?
				<xsl:choose>
					<xsl:when test="$aip-filepath[contains(FileName, '_pm')]">
						<xsl:analyze-string select="$aip-filepath/FileName[1]" regex="(rbrl\d{{2,5}}\w.**)_pm">
							<xsl:matching-substring>
								<xsl:value-of select="regex-group(1)"/>
								<xsl:text>_media</xsl:text>
							</xsl:matching-substring>
						</xsl:analyze-string>
					</xsl:when>
					<xsl:when test="//track[contains(FileExtension, 'xml') or contains(FileExtension, 'pdf') or contains(FileExtension, 'doc')]">
						<xsl:analyze-string select="$aip-filepath/FileName[1]" regex="(rbrl\d{{3}}\w{{2,5}}-\w[a-z0-9.%-]{{2,10}})_\w.**">
							<xsl:matching-substring>
								<xsl:value-of select="regex-group(1)"/>
								<xsl:text>_metadata</xsl:text>
							</xsl:matching-substring>
						</xsl:analyze-string>
					</xsl:when>
					<xsl:when test="$file-count > 1">
						<xsl:analyze-string select="$aip-filepath/FolderName" regex="(rbrl\d{{3}}\w{{2,5}}-\w.**)/objects">
							<xsl:matching-substring>
								<xsl:value-of select="regex-group(1)"/>
								<xsl:text>_media</xsl:text>
							</xsl:matching-substring>
						</xsl:analyze-string>
					</xsl:when>
					<xsl:otherwise>
						<xsl:analyze-string select="$aip-filepath/FileNameExtension" regex="(rbrl\d{{3}}\w{{2,5}}-\w**).\w{{2,3}}">
							<xsl:matching-substring>
								<xsl:value-of select="regex-group(1)"/>
							</xsl:matching-substring>
						</xsl:analyze-string>
					</xsl:otherwise>
				</xsl:choose>
			</dc:title>
		</xsl:if>-->
	</xsl:template>
	
	<xsl:template name="aip-id">
		<premis:objectIdentifier>
			<premis:objectIdentifierType><xsl:value-of select="$uri"/></premis:objectIdentifierType>
			<premis:objectIdentifierValue><xsl:value-of select="$aip-id"/></premis:objectIdentifierValue>
		</premis:objectIdentifier>
	</xsl:template>
	
	<xsl:template name="aip-version">
		<premis:objectIdentifier>
			<premis:objectIdentifierType>
				<xsl:value-of select="$uri"/>/<xsl:value-of select="$aip-id"/>
			</premis:objectIdentifierType>
			<premis:objectIdentifierValue>1</premis:objectIdentifierValue>
		</premis:objectIdentifier>
	</xsl:template>
	
	<xsl:template name="object-category">
		<premis:objectCategory>
			<xsl:if test="$file-count > 1">representation</xsl:if>
			<xsl:if test="$file-count = 1">file</xsl:if>
		</premis:objectCategory>
	</xsl:template>
	
	<xsl:template name="aip-size">
		<premis:size>
			<xsl:value-of select="format-number(sum(/MediaInfo/media/track[@type='General']/FileSize), '#')"/>
		</premis:size>
	</xsl:template>
	
	<xsl:template name="aip-unique-formats">
		<xsl:if test="$department = 'bmac'">
			<xsl:choose>
				<xsl:when test="//FileExtension = 'dpx'">
					<xsl:for-each select="/MediaInfo/media/track[@type='General']">
						<xsl:choose>
							<xsl:when test="Format='MPEG-4'">
								<premis:format>
									<premis:formatDesignation>
										<premis:formatName><xsl:value-of select="Format_Profile"/></premis:formatName>
									</premis:formatDesignation>
									<xsl:call-template name="mediainfo-note"/>
									<xsl:call-template name="codec-note"/>
								</premis:format>	
							</xsl:when>
							<xsl:when test="FileExtension='cue'">
								<premis:format>
									<premis:formatDesignation>
										<premis:formatName><xsl:value-of select="FileExtension"/></premis:formatName>
									</premis:formatDesignation>
									<xsl:call-template name="mediainfo-note"/>
								</premis:format>	
							</xsl:when>
							<xsl:otherwise>
								<premis:format>
									<premis:formatDesignation>
										<premis:formatName><xsl:value-of select="Format"/></premis:formatName>
										<xsl:if test="../track[@type='Video']/Format_Version">
											<premis:version>
												<xsl:value-of select="../track[@type='Video']/Format_Version"/>
											</premis:version>
										</xsl:if>
									</premis:formatDesignation>
									<xsl:call-template name="mediainfo-note"/>
								</premis:format>
							</xsl:otherwise>	
						</xsl:choose>
					</xsl:for-each>
				</xsl:when>
				<xsl:when test="//FileExtension = 'mkv'">
					<premis:format>
						<premis:formatDesignation>
							<premis:formatName>
								<xsl:value-of select="/MediaInfo/media/track[@type='General']/Format"/>
							</premis:formatName>
						</premis:formatDesignation>
						<xsl:call-template name="mediainfo-note"/>
						<xsl:call-template name="codec-note"/>					</premis:format>
				</xsl:when>
				<xsl:when test="//FileExtension = 'mov'">
					<premis:format>
						<premis:formatDesignation>
							<premis:formatName>
								<xsl:value-of select="/MediaInfo/media/track[@type='General']/Format_Profile"/>
							</premis:formatName>
							<xsl:call-template name="format-version"/>
						</premis:formatDesignation>
						<xsl:call-template name="mediainfo-note"/>
						<xsl:call-template name="codec-note"/>
					</premis:format>
				</xsl:when>
				<xsl:when test="//FileExtension = 'mxf'">
					<premis:format>
						<premis:formatDesignation>
							<premis:formatName>
								<xsl:value-of select="/MediaInfo/media/track[@type='General']/Format"/>
							</premis:formatName>
							<xsl:call-template name="format-version"/>
						</premis:formatDesignation>
						<xsl:call-template name="mediainfo-note"/>
						<xsl:call-template name="codec-note"/>
					</premis:format>	
				</xsl:when>
				<xsl:when test="//FileExtension = 'wav'">
					<premis:format>
						<premis:formatDesignation>
							<premis:formatName>
								<xsl:value-of select="/MediaInfo/media/track[@type='General']/Format"/>
							</premis:formatName>
							<xsl:call-template name="format-version"/>
						</premis:formatDesignation>
						<xsl:call-template name="mediainfo-note"/>
					</premis:format>
				</xsl:when>	
				<xsl:when test="//FileExtension = 'mp4'">
					<premis:format>
						<premis:formatDesignation>
							<premis:formatName>
								<xsl:value-of select="/MediaInfo/media/track[@type='General']/Format"/>
							</premis:formatName>
							<xsl:call-template name="format-version"/>
						</premis:formatDesignation>
						<xsl:call-template name="mediainfo-note"/>
						<xsl:call-template name="codec-note"/>
					</premis:format>
				</xsl:when>	

			</xsl:choose>
		</xsl:if>
		<xsl:if test="$department = 'rbrl'">
			<xsl:if test="$file-count = 1">
				<premis:format>
					<premis:formatDesignation>
						<premis:formatName><xsl:value-of select="$aip-filepath/Format"/></premis:formatName>
					</premis:formatDesignation>
					<xsl:call-template name="mediainfo-note"/>
				</premis:format>
			</xsl:if>
			<xsl:if test="$file-count > 1">
				<xsl:choose>
					<xsl:when test="//File[2]/track[1][not(contains(CompleteName, 'avchd'))]">
						<xsl:for-each-group select="//track[1]" group-by="Format">
							<xsl:sort select="current-grouping-key()"/>
							<premis:format>
								<premis:formatDesignation>
									<premis:formatName><xsl:value-of select="Format"/></premis:formatName>
								</premis:formatDesignation>
								<xsl:call-template name="mediainfo-note"/>
							</premis:format>
						</xsl:for-each-group>
						<xsl:for-each-group select="//track[1]" group-by="FileExtension[not(following-sibling::Format)]">
							<xsl:sort select="current-grouping-key()"/>
							<premis:format>
								<premis:formatDesignation>
									<premis:formatName><xsl:value-of select="FileExtension"/></premis:formatName>
								</premis:formatDesignation>
								<xsl:call-template name="mediainfo-note"/>
								<premis:formatNote>Unable to identify format. Instead, identified by file extension.</premis:formatNote>
							</premis:format>
						</xsl:for-each-group>
					</xsl:when>
					<xsl:when test="//File[2]/track[1][contains(CompleteName, 'avchd')]">
						<xsl:variable name="track2" select="/MediaInfo/File[1]/track[@type='Video'][1]"/>
						<premis:format>
							<premis:formatDesignation>
								<premis:formatName><xsl:value-of select="$aip-filepath/Format"/></premis:formatName>
							</premis:formatDesignation>
							<xsl:call-template name="mediainfo-note"/>
							<premis:formatNote>
								<xsl:text>File encoded as: </xsl:text>
								<xsl:value-of select="$track2/Encoded_Library, $track2/Format_Commercial, $track2/Format_Profile" separator=" "/>
								<xsl:text>.</xsl:text>
							</premis:formatNote>
						</premis:format>
						<premis:format>
							<premis:formatDesignation>
								<premis:formatName>AVCHD</premis:formatName>
							</premis:formatDesignation>
							<premis:formatNote>A complex directory format that is a composite of sub-component files, enumerated in the AIP-level file list.</premis:formatNote>
						</premis:format>
					</xsl:when>
				</xsl:choose>
			</xsl:if>
		</xsl:if>
	</xsl:template>
	
	<!--The next 3 templates are used for code for formats that repeats in multiple situations-->
	
	<!--QuickTime sometimes has a version value of 0. This does not have a real meaning and so is not included in the preservation.xml-->
	<xsl:template name="format-version">
		<xsl:if test="/MediaInfo/media[1]/track[@type='Video']/Format_Version and not(/MediaInfo/media[1]/track[@type='Video']/Format_Version = '0')">
			<premis:version>
				<xsl:value-of select="/MediaInfo/media[1]/track[@type='Video']/Format_Version"/>
			</premis:version>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="mediainfo-note">
		<premis:formatNote>
			<xsl:text>Format identified by Mediainfo version </xsl:text>
			<xsl:value-of select="/MediaInfo/creatingLibrary/@version"/>
			<xsl:text>.</xsl:text>
		</premis:formatNote>
	</xsl:template>
	
	<xsl:template name="codec-note">
		<premis:formatNote>
			<xsl:text>Video is encoded in the following codec: </xsl:text>
			<xsl:value-of select="/MediaInfo/media/track[@type='Video']/Format"/>
			<!--Matroska format uses Format_Version, while all other formats use Format_Profile, to supplement the Format description of the codec.-->
			<!--These are not always present, so tests if exists before selecting the value to avoid extra spacing in the note.-->
			<xsl:choose>
			  	<xsl:when test="//FileExtension = 'mkv' and /MediaInfo/media/track[@type='Video']/Format_Version">
			    		<xsl:text> version </xsl:text>
			    		<xsl:value-of select="/MediaInfo/media/track[@type='Video']/Format_Version"/>
			  	</xsl:when>
			  	<xsl:otherwise>
			    		<xsl:if test="//FileExtension != 'mp4' and /MediaInfo/media/track[@type='Video']/Format_Profile">
			      			<xsl:text> </xsl:text>
			      			<xsl:value-of select="/MediaInfo/media/track[@type='Video']/Format_Commercial"/>
			    		</xsl:if>
			  	</xsl:otherwise>  
			  </xsl:choose>
			<xsl:text>.</xsl:text>
		</premis:formatNote>
	</xsl:template>
	
	<xsl:template name="relationship-collection">
		<premis:relationship>
			<premis:relationshipType>structural</premis:relationshipType>
			<premis:relationshipSubType>Is Member Of</premis:relationshipSubType>
			<premis:relatedObjectIdentifier>
				<premis:relatedObjectIdentifierType><xsl:value-of select="$uri"/></premis:relatedObjectIdentifierType>
				<premis:relatedObjectIdentifierValue><xsl:value-of select="$collection-id"/></premis:relatedObjectIdentifierValue>
			</premis:relatedObjectIdentifier>
		</premis:relationship>
	</xsl:template>
	
	
	<!-- *************************************************************************************************************** -->
	<!-- *********************************************** FILELIST TEMPLATES ******************************************** -->
	<!-- *************************************************************************************************************** -->
	
	<!--This template makes the structure of the filelist, like match="/" does for the aip section.-->
	<xsl:template match="//track[@type='General']">
		<premis:object>
			<xsl:apply-templates select="../@ref"/>
			<xsl:call-template name="Category"/>
			<premis:objectCharacteristics>
				<xsl:apply-templates select="FileSize"/>
				<!--TODO: Add in RBRL format templates, where different-->
				<xsl:apply-templates select="Format_Profile[.='QuickTime'] | FileExtension[.='cue'] | Format[not(.='MPEG-4')]"/>
			</premis:objectCharacteristics>
			<xsl:call-template name="relationship-aip"/>
		</premis:object>
	</xsl:template>
	
	<xsl:template match="@ref">
		<premis:objectIdentifier>
			<premis:objectIdentifierType>
				<xsl:value-of select="$uri"/>/<xsl:value-of select="$aip-id"/>
			</premis:objectIdentifierType>
			<premis:objectIdentifierValue>
				<xsl:analyze-string select="." regex=".*/objects/([\w._-]*)">
					<xsl:matching-substring><xsl:sequence select="regex-group(1)"/></xsl:matching-substring>
				</xsl:analyze-string>
			</premis:objectIdentifierValue>
		</premis:objectIdentifier>	
	</xsl:template>
	
	<xsl:template name="Category">
		<xsl:choose>
			<xsl:when test="FileExtension = 'dpx'">
				<premis:objectCategory>representation</premis:objectCategory>
			</xsl:when>
			<xsl:otherwise>
			        <premis:objectCategory>file</premis:objectCategory>
			</xsl:otherwise>  
		</xsl:choose>	
	</xsl:template>
	
	<xsl:template match="FileSize">
		<premis:size><xsl:value-of select="format-number(., '#')"/></premis:size>
	</xsl:template>
	
	<!--TODO: Make these work for RBRL too-->
	
	<xsl:template match="Format_Profile">
		<premis:format>
			<premis:formatDesignation>
				<premis:formatName><xsl:value-of select="."/></premis:formatName>
			</premis:formatDesignation>
			<xsl:call-template name="mediainfo-note"/>
			<premis:formatNote>
				<xsl:text>Video is encoded in the following codec: </xsl:text>
				<xsl:value-of select="../following-sibling::track[@type='Video']/Format"/>
				<xsl:text> </xsl:text>
				<xsl:value-of select="../following-sibling::track[@type='Video']/Format_Profile"/>
				<xsl:text>.</xsl:text>
			</premis:formatNote>
		</premis:format>
	</xsl:template>

	<xsl:template match="FileExtension">
		<premis:format>
			<premis:formatDesignation>
				<premis:formatName><xsl:value-of select="."/></premis:formatName>
			</premis:formatDesignation>
			<xsl:call-template name="mediainfo-note"/>
			<premis:formatNote>This file contains the settings used for the film scan on the MWA Flashtranfer Choice machine.</premis:formatNote>
		</premis:format>
	</xsl:template>

	<xsl:template match="Format">
		<premis:format>
			<premis:formatDesignation>
				<premis:formatName><xsl:value-of select="."/></premis:formatName>
				<xsl:if test="../../track[@type='Video']/Format_Version and not(../../track[@type='Video']/Format_Version = '0')">
					<premis:version>
						<xsl:value-of select="../../track[@type='Video']/Format_Version"/>
					</premis:version>
				</xsl:if>
			</premis:formatDesignation>
			<xsl:call-template name="mediainfo-note"/>
		</premis:format>
	</xsl:template>	

	<xsl:template name="relationship-aip">
		<premis:relationship>
			<premis:relationshipType>structural</premis:relationshipType>
			<premis:relationshipSubType>Is Member Of</premis:relationshipSubType>
			<premis:relatedObjectIdentifier>
				<premis:relatedObjectIdentifierType><xsl:value-of select="$uri"/></premis:relatedObjectIdentifierType>
				<premis:relatedObjectIdentifierValue><xsl:value-of select="$aip-id"/></premis:relatedObjectIdentifierValue>
			</premis:relatedObjectIdentifier>
		</premis:relationship>
	</xsl:template>
	
</xsl:stylesheet>
