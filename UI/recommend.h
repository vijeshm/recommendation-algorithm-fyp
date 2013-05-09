#ifndef RECOMMEND_H
#define RECOMMEND_H

#include <QWidget>
#include "whythiswindow.h"
#include <QProcess>
namespace Ui {
class recommend;
}

class recommend : public QWidget
{
    Q_OBJECT
    
public:
    whythiswindow *whythiswin;
    QString value;
    QProcess *proc;
    QProcess *ythis;
    explicit recommend(QWidget *parent = 0);
    ~recommend();
    
private:
    Ui::recommend *ui;

public slots:
    void moveback();
    void openwindow();
    void alphachange();
    void recomm();
    void proccompleted();
    void ythisended();
signals:
    void movebacktoclusterusers();


};

#endif // RECOMMEND_H
