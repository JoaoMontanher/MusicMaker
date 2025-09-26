rm(list=ls())
library(shiny)
library(bslib)
library(reticulate)
py_require("mido")
py_require("pandas")
library(shinyjs)

chordsDB <- readxl::read_xlsx("chords.xlsx")
chordsDB[,1:3] <- chordsDB[,1:3] - 12

chords <- apply(chordsDB[,1:3],1,as.list)

chords <- lapply(chords,function(x) unlist(x))

chords <- setNames(chords,chordsDB$`Chord Name`)

mt <- list(c(480,480),960,rep(240,4))

# myAlgo <- function() {
#   times <- c()
#   while(sum(times) < 1920) {
#     times <- c(times,120*(2^sample(0:3,size=1)))
#   }
#   
#   if(sum(times) > 1920) {
#     times[length(times)] <- 1920 - sum(times[-length(times)])
#   }
#   
#   return(times)
# }

makeSession <- function(cds) {
  mld <- c()
  tt <- c()
  for (i in 1:length(cds)) {
    t <- unlist(sample(mt,replace=T,size=2))
    tt <- c(tt,t)
    mld <- c(mld,unlist(sample(unlist(chords[cds[i]]),replace = T,size=length(t))))
  }
  mld <- unname(mld+12)
  return(data.frame(mld,tt))
}

ui <- fluidPage(
  titlePanel("Music Generator"),
  card(
    card_header("Intro Chords"),
    selectInput("Intro1",label="Chord 1", choices = ls(chords)),
    selectInput("Intro2",label="Chord 2", choices = ls(chords)),
    selectInput("Intro3",label="Chord 3", choices = ls(chords)),
    selectInput("Intro4",label="Chord 4", choices = ls(chords)),
    sliderInput("repIntro", "Number of Intro Chords Repetitions", value = 4, min = 0, max = 8),
    
  ),
  card(
    card_header("Main Chords"),
    selectInput("Main1",label="Chord 1", choices = ls(chords)),
    selectInput("Main2",label="Chord 2", choices = ls(chords)),
    selectInput("Main3",label="Chord 3", choices = ls(chords)),
    selectInput("Main4",label="Chord 4", choices = ls(chords)),
    sliderInput("repMain", "Number of Main Chords Repetitions", value = 4, min = 0, max = 8),
  ),
  card(
    card_header("Chorus Chords"),
    selectInput("Chorus1",label="Chord 1", choices = ls(chords)),
    selectInput("Chorus2",label="Chord 2", choices = ls(chords)),
    selectInput("Chorus3",label="Chord 3", choices = ls(chords)),
    selectInput("Chorus4",label="Chord 4", choices = ls(chords)),
    sliderInput("repChorus", "Number of Chorus Chords Repetitions", value = 4, min = 0, max = 8),
  ),
  card(
    useShinyjs(),
    card_header("Config"),
    sliderInput("V", "5ª Probability", value = 50, min = 0, max = 100),
    #sliderInput("VII", "Probabilidade de 7ª", value = 50, min = 0, max = 100),
    sliderInput("VIII", "8ª Probability", value = 50, min = 0, max = 100),
    radioButtons("seed", "Will you use a seed?",
                 choices = c("No" = "disable","Yes" = "enable")),
    textInput("seedValue", "Type your Seed:"),
    radioButtons("bassType","Which bass chord pattern would you use?",
                 choices = c("Simple","Random Repeated"))
  ),
  
  downloadButton("download","Download .mid File"),
  p("\n"),
  p("Ko-Fi: https://ko-fi.com/joaomontanher"),
  p("Pix: joaocatapan@protonmail.com"),
  p("MIT License Copyright (c) 2025 João Pedro Catapan Montanher (joaocatapan@protonmail.com)"))

server <- function(input, output) {
  
  observe({
    shinyjs::toggleState("seedValue", condition = (input$seed == "enable"))
  })
  
  output$download <- downloadHandler(

    filename = function() {
      "Music.mid"
    },
    content = function(file) {
      random_string <- paste(sample(c(letters, 0:9), 10, replace = TRUE), collapse = "")
      name <- digest::digest(random_string, algo = "md5")
      
      if (input$seedValue != "") {
        set.seed(as.numeric(input$seedValue))
      }
      
      chordsIntro <- c(input$Intro1,input$Intro2,input$Intro3,input$Intro4)
      Intro <- makeSession(chordsIntro)
      
      chordsMain <- c(input$Main1,input$Main2,input$Main3,input$Main4)
      Main <- makeSession(chordsMain)
      #Bridge <- makeSession(c(input$Intro1,input$Intro2,input$Intro3,input$Intro4))
      chordsChorus <- c(input$Chorus1,input$Chorus2,input$Chorus3,input$Chorus4)
      Chorus <- makeSession(chordsChorus)
      
      
      reps <- c(rep(chordsIntro,input$repIntro),rep(chordsMain,input$repMain),rep(chordsChorus,input$repChorus),rep(chordsMain,input$repMain),rep(chordsChorus,input$repChorus),rep(chordsIntro,input$repIntro))
      #print(reps)
      
      finalMelodies <- rbind(rep(Intro,input$repIntro),rep(Main,input$repMain),rep(Chorus,input$repChorus),rep(Main,input$repMain),rep(Chorus,input$repChorus),rep(Intro,input$repIntro))
      
      finalIntro <- do.call(rbind, replicate(input$repIntro,Intro, simplify = FALSE))
      finalMain <- do.call(rbind, replicate(input$repMain,Main, simplify = FALSE))
      finalChorus <- do.call(rbind, replicate(input$repChorus,Chorus, simplify = FALSE))
      
      finalMelodies <- rbind(finalIntro,finalMain,finalChorus,finalMain,finalChorus,finalIntro)
      
      FinalChords <- chords[reps]
      
      #print(chordsFinais)
      
      finalChords <- cbind(as.data.frame(do.call(rbind, FinalChords)))
      
      system(paste("mkdir",name))
      system(paste0("cp main.py ",name,"/"))
      
      #basicData <- data.frame(V = input$V,VII = input$VII,VIII = input$VIII)
      
      #print(finalMelodies)
      
      finalV <- (rbinom(nrow(finalMelodies),1,input$V/100) * (finalMelodies$mld + 7))
      #finalVII <- (rbinom(nrow(finalMelodies),1,input$VII/100) * (finalMelodies[,1]+11))
      finalVIII <- (rbinom(nrow(finalMelodies),1,input$VIII/100) * (finalMelodies$mld +12))

      finalMelodies <- cbind(finalMelodies,finalV,finalVIII)

      setwd(name)
      
      #chordTimes <- data.frame(myAlgo())
      # "Random Repeated" "Simple"
      
      if (input$bassType == "Simple") {
        bassType <- data.frame(bassType="Simple")
      } else if (input$bassType == "Random Repeated") {
        bassType <- data.frame(bassType="Random Repeated")
      }
      
      #write.table(chordTimes,"chordTimes.csv",sep=";")
      write.table(finalMelodies,"melodies.csv",sep=';')
      write.table(finalChords,"chords.csv",sep=';')
      write.table(bassType,"bassType.csv",sep=";")
      #write.table(basicData,"basicData.csv",sep=";")
      
      py_run_file("main.py")
      
      file.copy("Music.mid",file)
      
      setwd("..")
      #getwd()
      system(paste0("rm -r ",name))
      
    })
}

shinyApp(ui = ui, server = server)
